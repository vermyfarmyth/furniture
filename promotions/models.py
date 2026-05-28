from django.db import models

from catalog.models import Product


class Promotion(models.Model):
    title = models.CharField(max_length=120)
    discount_percent = models.PositiveSmallIntegerField(default=10)
    active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product, related_name='promotions', blank=True)


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    discount_percent = models.PositiveSmallIntegerField(default=10)
    is_active = models.BooleanField(default=True)
