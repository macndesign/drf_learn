from __future__ import unicode_literals
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Product, ProductModel, Order, CoreRouter


class CoreRouterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)

    def create(self, validated_data):
        return CoreRouter(name=None)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
