from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.shortcuts import render

from catalog.models import Product
from orders.models import Order
from reviews.models import Review


@user_passes_test(lambda user: user.is_staff)
def index(request):
    top_products = Product.objects.annotate(review_count=Count('reviews')).order_by('-review_count')[:5]
    return render(
        request,
        'dashboard/index.html',
        {
            'orders_count': Order.objects.count(),
            'reviews_count': Review.objects.count(),
            'top_products': top_products,
        },
    )
