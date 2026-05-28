import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from catalog.models import Category, Product
from favorites.models import Favorite
from reviews.models import Review


def _error(message, status=400):
    return JsonResponse({'error': {'message': message, 'status': status}}, status=status)


def products_api(request):
    queryset = Product.objects.select_related('category', 'brand')
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    brand = request.GET.get('brand', '').strip()
    sort = request.GET.get('sort', '-created_at').strip()
    min_price = request.GET.get('min_price', '').strip()

    if q:
        queryset = queryset.filter(title__icontains=q)
    if category:
        queryset = queryset.filter(category__slug=category)
    if brand:
        queryset = queryset.filter(brand__slug=brand)
    if min_price.replace('.', '', 1).isdigit():
        queryset = queryset.filter(price__gte=min_price)
    if sort in ['price', '-price', 'title', '-created_at', 'created_at']:
        queryset = queryset.order_by(sort)

    paginator = Paginator(queryset, int(request.GET.get('limit', 10)))
    page_obj = paginator.get_page(request.GET.get('page', 1))

    return JsonResponse(
        {
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'results': [
                {
                    'id': p.id,
                    'title': p.title,
                    'slug': p.slug,
                    'category': p.category.name,
                    'price': float(p.price),
                    'is_available': p.is_available,
                }
                for p in page_obj
            ],
        }
    )


def product_detail_api(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return JsonResponse(
        {
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'category': product.category.name,
            'brand': product.brand.name,
            'price': float(product.price),
            'year': product.year,
            'stock': product.stock,
        }
    )


def categories_api(request):
    return JsonResponse({'results': list(Category.objects.values('id', 'name', 'slug'))})


def reviews_api(request):
    payload = list(Review.objects.select_related('user', 'product').values('id', 'rating', 'text', 'user__username', 'product__slug')[:50])
    return JsonResponse({'results': payload})


@login_required
def favorites_api(request):
    payload = list(Favorite.objects.filter(user=request.user).select_related('product').values('product__title', 'product__slug'))
    return JsonResponse({'results': payload})


@csrf_exempt
@require_http_methods(['POST'])
@login_required
def product_create_api(request):
    if not request.user.is_staff:
        return _error('Недостаточно прав', 403)
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return _error('Некорректный JSON', 400)

    required = ['title', 'slug', 'category_id', 'brand_id', 'price', 'description', 'year']
    for field in required:
        if field not in body:
            return _error(f'Поле {field} обязательно', 400)

    try:
        product = Product.objects.create(
            title=body['title'],
            slug=body['slug'],
            category_id=body['category_id'],
            brand_id=body['brand_id'],
            price=body['price'],
            description=body['description'],
            year=body['year'],
            stock=body.get('stock', 0),
        )
    except Exception as exc:
        return _error(str(exc), 400)

    return JsonResponse({'id': product.id, 'slug': product.slug}, status=201)


@csrf_exempt
@require_http_methods(['PUT', 'DELETE'])
@login_required
def product_manage_api(request, slug):
    if not request.user.is_staff:
        return _error('Недостаточно прав', 403)

    product = get_object_or_404(Product, slug=slug)

    if request.method == 'DELETE':
        product.delete()
        return JsonResponse({'message': 'Удалено'})

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return _error('Некорректный JSON', 400)

    for field in ['title', 'description', 'price', 'stock', 'year', 'is_available']:
        if field in body:
            setattr(product, field, body[field])
    product.save()
    return JsonResponse({'message': 'Обновлено'})
