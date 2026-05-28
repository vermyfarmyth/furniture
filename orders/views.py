from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Order


@login_required
def my_orders(request):
    return render(request, 'orders/list.html', {'orders': Order.objects.filter(user=request.user).prefetch_related('items__product')})
