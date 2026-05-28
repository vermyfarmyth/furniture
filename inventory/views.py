from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from .models import Delivery, Inventory


def is_staff(user):
    return user.is_staff


@user_passes_test(is_staff)
def inventory_dashboard(request):
    inventories = Inventory.objects.select_related('warehouse', 'product')[:30]
    deliveries = Delivery.objects.select_related('warehouse', 'product')[:10]
    return render(request, 'inventory/dashboard.html', {'inventories': inventories, 'deliveries': deliveries})
