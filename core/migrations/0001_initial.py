# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from . import initial_data


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=75)),
            ],
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('product', models.ForeignKey(to='core.Product', related_name='models')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product_models',
            field=models.ManyToManyField(to='core.ProductModel', related_name='product_models'),
        ),
        migrations.RunPython(initial_data)
    ]
