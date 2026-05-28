from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Product

from .models import Favorite


@login_required
def toggle_favorite(request, slug):
    product = get_object_or_404(Product, slug=slug)
    fav, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        fav.delete()
    return redirect('catalog:detail', slug=slug)


@login_required
def list_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'favorites/list.html', {'favorites': favorites})
