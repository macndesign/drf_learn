from django.db import models


class CoreRouter(object):
    def __init__(self, name):
        self.name = name


class Product(models.Model):
    name = models.CharField(max_length=75)

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    name = models.CharField(max_length=120)
    product = models.ForeignKey('core.Product', related_name='models')

    def __str__(self):
        return '{} {}'.format(self.product.name, self.name)


class Order(models.Model):
    address = models.TextField()
    product_models = models.ManyToManyField('core.ProductModel', related_name='product_models')

    def __str__(self):
        return 'Id: {}, Address: {}'.format(self.pk, self.address)
