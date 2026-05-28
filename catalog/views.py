from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from reviews.forms import ReviewForm
from .forms import ProductForm
from .models import Category, Product


def product_list(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '')
    sort = request.GET.get('sort', '-created_at')
    year = request.GET.get('year', '')

    products = Product.objects.select_related('category', 'brand').prefetch_related('materials', 'colors')

    if query:
        products = products.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(brand__name__icontains=query))
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if year.isdigit():
        products = products.filter(year=int(year))
    if sort in ['price', '-price', 'title', '-created_at', 'created_at']:
        products = products.order_by(sort)

    paginator = Paginator(products, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(
        request,
        'catalog/product_list.html',
        {
            'page_obj': page_obj,
            'categories': Category.objects.all(),
            'query': query,
            'category_slug': category_slug,
            'sort': sort,
            'year': year,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category', 'brand').prefetch_related('materials', 'colors', 'tags', 'features', 'images'),
        slug=slug,
    )
    avg_rating = product.reviews.aggregate(avg=Avg('rating')).get('avg') or 0
    reviews = product.reviews.select_related('user')
    review_form = None
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        review_form = ReviewForm(instance=user_review)
    return render(
        request,
        'catalog/product_detail.html',
        {
            'product': product,
            'avg_rating': round(avg_rating, 1),
            'reviews': reviews,
            'review_form': review_form,
            'user_review': user_review,
        },
    )


@login_required
@permission_required('catalog.add_product', raise_exception=True)
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Товар создан.')
        return redirect('catalog:list')
    return render(request, 'catalog/product_form.html', {'form': form, 'title': 'Создать товар'})


@login_required
@permission_required('catalog.change_product', raise_exception=True)
def product_update(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Товар обновлен.')
        return redirect('catalog:detail', slug=product.slug)
    return render(request, 'catalog/product_form.html', {'form': form, 'title': 'Редактировать товар'})


@login_required
@permission_required('catalog.delete_product', raise_exception=True)
def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Товар удален.')
        return redirect('catalog:list')
    return render(request, 'catalog/product_delete.html', {'product': product})


def quick_search(request):
    term = request.GET.get('term', '')
    data = list(Product.objects.filter(title__icontains=term).values('title', 'slug')[:10])
    from django.http import JsonResponse

    return JsonResponse({'results': data})
