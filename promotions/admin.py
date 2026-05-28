from django.contrib import admin

from .models import Coupon, Promotion


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_percent', 'active')
    list_filter = ('active',)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'is_active')
    search_fields = ('code',)
