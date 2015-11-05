# coding: utf-8
from __future__ import unicode_literals, absolute_import
import os
import boto
from boto.s3.key import Key
import requests
import shutil
from filechunkio import FileChunkIO
import math
from .common import AWSConfig, AWSError


class S3BucketConfig(AWSConfig):
    def __init__(self, bucket_name):
        super(S3BucketConfig, self).__init__('s3')
        self.bucket_name = bucket_name
        self.bucket_object = None

    def bucket(self):
        try:
            self.bucket_object = self.connect().get_bucket(self.bucket_name)
        except boto.exception.S3ResponseError:
            try:
                self.bucket_object = self.connect().create_bucket(self.bucket_name)
                self.bucket_object.set_canned_acl('public-read')
            except boto.exception.S3CreateError:
                raise AWSError('Error on bucket creation')

        return self.bucket_object


class S3BucketFileSend(S3BucketConfig):
    def __init__(self, bucket_name, download_url, download_to):
        super(S3BucketFileSend, self).__init__(bucket_name)
        self.download_url = download_url
        self.download_to = download_to
        self.file_name = os.path.basename(self.download_to)

    def save_file(self):
        r = requests.get(self.download_url, stream=True)
        with open(self.download_to, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

        return r.status_code

    def source_size(self):
        return os.stat(self.download_to).st_size

    def upload(self):
        multi_part = self.bucket().initiate_multipart_upload(self.file_name)

        chunk_size = 52428800
        chunk_count = int(math.ceil(self.source_size() / float(chunk_size)))

        for i in range(chunk_count):
            offset = chunk_size * i
            byte_set = min(chunk_size, self.source_size() - offset)
            with FileChunkIO(self.download_to, 'r', offset=offset, bytes=byte_set) as f:
                multi_part.upload_part_from_file(f, part_num=i + 1)

        k = Key(self.bucket())
        k.name = self.file_name
        k.set_contents_from_filename(self.file_name, policy='public-read')
        multi_part.complete_upload()

        return k.name

    def as_view(self):
        self.save_file()
        self.upload()
        if os.path.exists(self.download_to):
            os.remove(self.download_to)


# if __name__ == '__main__':
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#
#     URL = 'https://www.python.org/static/community_logos/python-logo.png'
#     FILE_NAME = URL.split('/')[-1]
#     FILE_PATH = os.path.join(BASE_DIR, FILE_NAME)
#
#     os.environ['AWS_APP_KEY'] = 'AWS_APP_KEY'
#     os.environ['AWS_SECRET_KEY'] = 'AWS_SECRET_KEY'
#     send = S3BucketFileSend('l-labs', URL, FILE_PATH)
#     send.as_view()
