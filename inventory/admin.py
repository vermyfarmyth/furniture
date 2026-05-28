from django.contrib import admin

from .models import Delivery, Inventory, Warehouse


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('warehouse', 'product', 'quantity')
    search_fields = ('warehouse__name', 'product__title')


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('warehouse', 'product', 'expected_date', 'quantity')
    list_filter = ('expected_date',)
