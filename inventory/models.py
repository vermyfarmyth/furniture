from django.db import models

from catalog.models import Product


class Warehouse(models.Model):
    name = models.CharField(max_length=120)
    city = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='inventories')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventories')
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('warehouse', 'product')


class Delivery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    expected_date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
