from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Product
from .forms import ReviewForm
from .models import Review


@login_required
def my_reviews(request):
    return render(request, 'reviews/list.html', {'reviews': Review.objects.filter(user=request.user).select_related('product')})


@login_required
def add_review(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category', 'brand').prefetch_related('materials', 'colors', 'tags', 'features', 'images'),
        slug=slug,
    )
    existing = Review.objects.filter(user=request.user, product=product).first()
    form = ReviewForm(request.POST or None, instance=existing)
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.product = product
        review.save()
        messages.success(request, 'Спасибо! Отзыв сохранен.')
        return redirect('catalog:detail', slug=product.slug)

    avg_rating = product.reviews.aggregate(avg=Avg('rating')).get('avg') or 0
    return render(
        request,
        'catalog/product_detail.html',
        {
            'product': product,
            'avg_rating': round(avg_rating, 1),
            'reviews': product.reviews.select_related('user'),
            'review_form': form,
            'user_review': existing,
        },
    )
