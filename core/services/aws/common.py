# coding: utf-8
from __future__ import unicode_literals, absolute_import
import os
import boto


class AWSError(Exception):
    pass


class AWSConfig(object):
    def __init__(self, service):
        self.app_key = os.getenv('AWS_APP_KEY')
        self.secret_key = os.getenv('AWS_SECRET_KEY')
        self.service = service
        self.conn = None

    def connect(self):
        try:
            self.conn = getattr(boto, 'connect_' + self.service)(self.app_key, self.secret_key)
            print(self.conn)
        except boto.exception.AWSConnectionError:
            raise AWSError('Error on connection')

        return self.conn
