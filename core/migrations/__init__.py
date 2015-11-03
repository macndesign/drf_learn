from __future__ import unicode_literals
from django.contrib.auth.hashers import make_password


def initial_data(apps, schema_editor):
    user = apps.get_model('auth', 'User')
    product = apps.get_model('core', 'Product')
    product_model = apps.get_model('core', 'ProductModel')
    order = apps.get_model('core', 'Order')

    # Creating initial User
    user = user(username='admin', email='admin@admin.com')
    user.password = make_password('admin')
    user.is_superuser = True
    user.is_staff = True
    user.save()

    # Creating models and products for iPhone
    iphone = product.objects.create(name='iPhone')
    iphone_4s = product_model.objects.create(name='4S', product=iphone)
    iphone_5c = product_model.objects.create(name='5C', product=iphone)
    iphone_6s = product_model.objects.create(name='6S', product=iphone)

    # Creating models and products for Dell
    dell = product.objects.create(name='Dell')
    vostro = product_model.objects.create(name='Vostro', product=dell)
    inspiron = product_model.objects.create(name='Inspiron', product=dell)

    # Creating orders
    order1 = order.objects.create(address='123, My Street1, City1, Country1')
    order1.product_models.add(iphone_4s, inspiron, iphone_5c)

    order2 = order.objects.create(address='456, My Street2, City2, Country2')
    order2.product_models.add(vostro, iphone_6s)
