# coding: utf-8
from __future__ import unicode_literals, absolute_import
import os
from functools import wraps
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .services.aws.s3 import S3BucketFileSend


class CoreRouter(object):
    def __init__(self, name):
        self.name = name


class Product(models.Model):
    name = models.CharField(max_length=75)

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    name = models.CharField(max_length=120)
    image_url = models.URLField(max_length=250, blank=True)
    product = models.ForeignKey('core.Product', related_name='models')

    def __str__(self):
        return '{} {}'.format(self.product.name, self.name)


def download_and_send_to_s3(image_url):
    bucket = 'l-labs'
    file_name = image_url.split('/')[-1]
    file_path = os.path.join(settings.BASE_DIR, file_name)
    send = S3BucketFileSend(bucket, image_url, file_path)
    send.as_view()
    return 'https://s3.amazonaws.com/' + bucket + '/' + file_name


def skip_signal():
    def _skip_signal(signal_func):
        @wraps(signal_func)
        def _decorator(sender, instance, **kwargs):
            if hasattr(instance, 'skip_signal'):
                return None
            return signal_func(sender, instance, **kwargs)
        return _decorator
    return _skip_signal


@receiver(post_save, sender=ProductModel)
@skip_signal()
def product_model_post_save(sender, instance, **kwargs):
    # https://www.python.org/static/community_logos/python-logo.png
    s3_url = download_and_send_to_s3(instance.image_url)
    instance.image_url = s3_url
    instance.skip_signal = True
    instance.save()


class Order(models.Model):
    address = models.TextField()
    product_models = models.ManyToManyField('core.ProductModel', related_name='product_models')

    def __str__(self):
        return 'Id: {}, Address: {}'.format(self.pk, self.address)
