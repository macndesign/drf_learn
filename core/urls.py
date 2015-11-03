from rest_framework import routers
from django.conf.urls import url, include
from .views import ProductViewSet, ProductModelViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, base_name='product')
router.register(r'product-models', ProductModelViewSet, base_name='product-model')
router.register(r'orders', OrderViewSet, base_name='order')

urlpatterns = [
    url(r'^', include(router.urls)),
]
