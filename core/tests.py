from django.test import TestCase
from .models import Product, ProductModel, Order
from django.contrib.auth.models import User


class CoreModelTestCase(TestCase):
    def setUp(self):

        # Creating models and products for iPhone
        self.iphone = Product.objects.create(name='iPhone')
        self.iphone_4s = ProductModel.objects.create(name='4S', product=self.iphone)
        self.iphone_5c = ProductModel.objects.create(name='5C', product=self.iphone)
        self.iphone_6s = ProductModel.objects.create(name='6S', product=self.iphone)

        # Creating models and products for Dell
        self.dell = Product.objects.create(name='Dell')
        self.vostro = ProductModel.objects.create(name='Vostro', product=self.dell)
        self.inspiron = ProductModel.objects.create(name='Inspiron', product=self.dell)

        # Creating orders
        self.order1 = Order.objects.create(address='123, My Street1, City1, Country1')
        self.order1.product_models.add(self.iphone_4s, self.iphone_5c, self.iphone_6s)

        self.order2 = Order.objects.create(address='456, My Street2, City2, Country2')
        self.order2.product_models.add(self.vostro, self.inspiron)

    def test_should_fetch_all_product_models_for_each_order(self):
        self.assertEqual(self.order1.product_models.count(), 3)
        self.assertEqual(self.order2.product_models.count(), 2)

    def test_should_fetch_correct_product_models_for_each_order(self):
        self.assertEqual(list(self.order1.product_models.values_list('name')), [('4S',), ('5C',), ('6S',)])
        self.assertEqual(list(self.order2.product_models.values_list('name')), [('Vostro',), ('Inspiron',)])


class CoreClientTestCase(TestCase):
    pass
