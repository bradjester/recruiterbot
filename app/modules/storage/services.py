# -*- coding: utf-8 -*-
"""
    app.modules.storage.services
    ~~~~~~~~~~~~~~

    Storage module services
"""
import os

import magic
from flask import current_app

from .constants import JOB_CANDIDATE_RESUME_PATH_FMT, JOB_BANNER_PATH_FMT, \
    JOB_DESCRIPTION_PATH_FMT, JOB_CANDIDATE_FILES_PREFIX
from .errors import AppUploadFailedFileExistsError


class StaticStorageService(object):
    _magic_mime = None

    def __init__(self, s3_service):
        super(StaticStorageService, self).__init__()
        self.s3_service = s3_service

    def generate_signed_url(self, key):
        if not key:
            return None
        return self.s3_service.generate_object_signed_url(self._bucket, key)

    def generate_job_description_signed_post(
            self, job_uuid, file_name, overwrite=False, content_type=None):
        key = self.get_job_description_key(job_uuid, file_name)
        return self.generate_signed_post(
            key, overwrite=overwrite, content_type=content_type)

    def get_job_description_key(self, job_uuid, file_name):
        return JOB_DESCRIPTION_PATH_FMT.format(
            job_uuid, self.s3_service.sanitize_key(file_name))

    def generate_job_banner_signed_post(
            self, job_uuid, file_name, overwrite=True, content_type=None):
        key = self.get_job_banner_key(job_uuid, file_name)
        return self.generate_signed_post(
            key, overwrite=overwrite, content_type=content_type)

    def get_job_banner_key(self, job_uuid, file_name):
        return JOB_BANNER_PATH_FMT.format(
            job_uuid, self.s3_service.sanitize_key(file_name))

    def generate_job_candidate_resume_signed_post(
        self, job_uuid, session_id, file_name, overwrite=False,
            content_type=None):
        key = self.get_job_candidate_resume_key(job_uuid, session_id,
                                                file_name)
        return self.generate_signed_post(
            key, overwrite=overwrite, content_type=content_type)

    def get_job_candidate_resume_key(self, job_uuid, session_id, file_name):
        return JOB_CANDIDATE_RESUME_PATH_FMT.format(
            job_uuid, session_id, self.s3_service.sanitize_key(file_name))

    def generate_signed_post(self, key, overwrite=False, content_type=None):
        if not overwrite:
            self._error_if_exists(key)
        return self.s3_service.generate_signed_post(
            self._bucket, key, content_type=content_type)

    def copy_from_url(self, url, job_uuid, session_id):
        prefix = JOB_CANDIDATE_FILES_PREFIX.format(job_uuid, session_id)
        return self.s3_service.copy_from_url(url, self._bucket, prefix)

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
        return current_app.config.get('APP_AWS_S3_BUCKET')

    @property
    def _mime(self):
        if not self._magic_mime:
            self._magic_mime = magic.Magic(mime=True)
        return self._magic_mime
