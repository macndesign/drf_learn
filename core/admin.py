from django.contrib import admin
from .models import Product, ProductModel, Order


class ProductModelAdmin(admin.TabularInline):
    model = ProductModel


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductModelAdmin]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
