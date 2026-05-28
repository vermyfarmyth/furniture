from django.db.models import Avg, Count
from django.shortcuts import render

from catalog.models import Brand, Category, Product


def home(request):
    featured_products = Product.objects.select_related('category', 'brand').prefetch_related('materials')[:8]
    stats = Category.objects.annotate(products_count=Count('products')).order_by('-products_count')[:6]
    avg_rating = Product.objects.aggregate(avg=Avg('reviews__rating')).get('avg') or 0
    return render(
        request,
        'core/home.html',
        {
            'featured_products': featured_products,
            'category_stats': stats,
            'brand_count': Brand.objects.count(),
            'avg_rating': round(avg_rating, 1),
        },
    )


def about(request):
    return render(request, 'core/about.html')


def contacts(request):
    return render(request, 'core/contacts.html')


def project_page(request):
    return render(request, 'core/project.html')


def error_404(request, exception):
    return render(request, 'errors/404.html', status=404)


def error_404_preview(request):
    return render(request, 'errors/404.html', status=404)


def error_500(request):
    return render(request, 'errors/500.html', status=500)
