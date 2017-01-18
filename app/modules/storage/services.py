# -*- coding: utf-8 -*-
"""
    app.modules.storage.services
    ~~~~~~~~~~~~~~

    Storage module services
"""
import os

import magic
from flask import current_app

from .constants import USER_CV_PATH_FMT
from .errors import AppUploadFailedFileExistsError


class StaticStorageService(object):
    _magic_mime = None

    def __init__(self, s3_service):
        super(StaticStorageService, self).__init__()
        self.s3_service = s3_service

    def generate_signed_url(self, key):
        return self.s3_service.generate_object_signed_url(self._bucket, key)

    def generate_user_cv_signed_post(
            self, client, file_name, overwrite=False, content_type=None):
        key = self.get_user_cv_key(client, file_name)
        return self.generate_signed_post(
            key, overwrite=overwrite, content_type=content_type)

    def get_user_cv_key(self, client, file_name):
        return USER_CV_PATH_FMT.format(
            client.id, self.s3_service.sanitize_key(file_name))

    def generate_signed_post(self, key, overwrite=False, content_type=None):
        if not overwrite:
            self._error_if_exists(key)
        return self.s3_service.generate_signed_post(
            self._bucket, key, content_type=content_type)

    def upload_user_cv(self, filename, client, overwrite=False):
        key = USER_CV_PATH_FMT.format(client.id, self._basename(filename))
        return self._upload_file(filename, key, overwrite=overwrite)

    @staticmethod
    def _basename(filename):
        return os.path.basename(filename)

    def _upload_file(self, filename, key, overwrite=False):
        if not overwrite:
            self._error_if_exists(key)
        mime_type = self._get_mime_type(filename)
        return self.s3_service.upload_file(
            filename, self._bucket, key, extra_args={'ContentType': mime_type})

    def _error_if_exists(self, key):
        if self.s3_service.object_exists(self._bucket, key):
            raise AppUploadFailedFileExistsError(
                'Upload failed, overwrite is not True and file already exists '
                'on S3: {}/{}'.format(self._bucket, key))

    def _get_mime_type(self, filename):
        return self._mime.from_file(filename)

    @property
    def _bucket(self):
        return current_app.config.get('AWS_S3_BUCKET')

    @property
    def _mime(self):
        if not self._magic_mime:
            self._magic_mime = magic.Magic(mime=True)
        return self._magic_mime
