from django.contrib import admin

from .models import Product, ProductPrice, ProductType, Unit


class ProductPriceInline(admin.TabularInline):
    model = ProductPrice
    fields = ['price', 'min_amount']
    extra = 1


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'unit', 'is_archived']
    search_fields = ['name']
    list_filter = ['type', 'is_archived']
    inlines = [ProductPriceInline]
    autocomplete_fields = ['type']
