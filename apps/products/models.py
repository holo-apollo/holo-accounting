from django.contrib.postgres.fields import CICharField
from django.db import models


class Unit(models.Model):
    name = CICharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = CICharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = CICharField(max_length=254, unique=True)
    type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name='products')
    description = models.TextField(null=True, blank=True, default='')
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='products')
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name + (' (archived)' if self.is_archived else '')


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    min_amount = models.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        ordering = ['min_amount']

    def __str__(self):
        return f'{self.product} costs {self.price} UAH from {self.min_amount} {self.product.unit}s'
