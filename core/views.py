from __future__ import unicode_literals
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from .models import Product, ProductModel, Order, CoreRouter
from .serializers import UserSerializer, GroupSerializer, ProductSerializer, ProductModelSerializer, OrderSerializer, \
    CoreRouterSerializer
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy


routers = {
    1: CoreRouter(name=reverse_lazy('product-list')),
    2: CoreRouter(name=reverse_lazy('product-model-list')),
    3: CoreRouter(name=reverse_lazy('order-list')),
}


class CoreRouterViewSet(viewsets.ViewSet):
    serializer_class = CoreRouterSerializer

    def list(self, request):
        serializer = CoreRouterSerializer(instance=routers.values(), many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
