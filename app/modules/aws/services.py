# -*- coding: utf-8 -*-
"""
    app.modules.aws.services
    ~~~~~~~~~~~~~~

    AWS module services
"""
import re

import boto3
from boto3.exceptions import S3UploadFailedError
from boto3.s3.transfer import S3Transfer
from botocore.exceptions import ClientError
from flask import current_app

from .constants import S3_LEGAL_KEY_CHARACTERS
from .errors import AppUploadFailedError


class AWSS3Service(object):
    def __init__(self, aws_service):
        super(AWSS3Service, self).__init__()
        self.aws_service = aws_service

    @staticmethod
    def sanitize_key(key):
        return re.sub(S3_LEGAL_KEY_CHARACTERS, '', key)

    def object_exists(self, bucket, key):
        try:
            self.aws_service.s3.meta.client.head_object(Bucket=bucket, Key=key)
        except ClientError:
            return False
        return True

    def generate_object_signed_url(self, bucket, key):
        return self.aws_service.s3.meta.client.generate_presigned_url(
            'get_object', Params={'Bucket': bucket, 'Key': key})

    def generate_signed_post(self, bucket, key, content_type=None):
        fields = {}
        conditions = []
        if content_type:
            fields['Content-Type'] = content_type
            conditions.append({'Content-Type': content_type})
        return self.aws_service.s3.meta.client.generate_presigned_post(
            Bucket=bucket, Key=self.sanitize_key(key), Fields=fields,
            Conditions=conditions)

    def upload_file(self, filename, bucket, key, extra_args=None):
        clean_key = self.sanitize_key(key)
        try:
            S3Transfer(self.aws_service.s3.meta.client).upload_file(
                filename, bucket, clean_key, extra_args=extra_args)
        except S3UploadFailedError as e:
            raise AppUploadFailedError("Failed to upload file to S3") from e
        return clean_key


class AWSSESService(object):
    def __init__(self, aws_service):
        super(AWSSESService, self).__init__()
        self.aws_service = aws_service

    def send_message(self, msg):
        config = current_app.config
        msg.charset = msg.charset if msg.charset else 'UTF-8'
        params = dict(
            Source=msg.sender,
            Destination=dict(
                ToAddresses=msg.recipients,
                CcAddresses=msg.cc,
                BccAddresses=msg.bcc
            ),
            Message=dict(
                Subject=dict(
                    Data=msg.subject,
                    Charset=msg.charset
                ),
                Body=dict(
                    Text=dict(
                        Data=msg.body,
                        Charset=msg.charset
                    ),
                    Html=dict(
                        Data=msg.html,
                        Charset=msg.charset
                    )
                )
            ),
            ReturnPath=config.get('BOUNCES_AND_COMPLAINTS_EMAIL')
        )
        if msg.reply_to:
            params['ReplyToAddresses'] = [msg.reply_to]
        self.send_email(**params)

    def send_email(self, **kwargs):
        self.aws_service.ses.send_email(**kwargs)


class AWSService(object):
    _default_session = None
    _us_west_session = None

    @property
    def s3(self):
        return self._default_aws_session.resource('s3')

    @property
    def ses(self):
        return self._us_west_aws_session.client('ses')

    @property
    def _default_aws_session(self):
        if not self._default_session:
            self._default_session = self._create_session()
        return self._default_session

    @property
    def _us_west_aws_session(self):
        if not self._us_west_session:
            self._us_west_session = self._create_session(region='us-west-2')
        return self._us_west_session

    @staticmethod
    def _create_session(region=None):
        config = current_app.config
        # If we are in DEV environment then get the key id and secret from the
        # config. Otherwise, set it to None and allow boto3 to get it from AWS
        # EC2 metadata.
        key_id = None
        secret = None
        if config.get('IS_DEV'):
            key_id = config.get('APP_AWS_ACCESS_KEY_ID')
            secret = config.get('APP_AWS_SECRET_ACCESS_KEY')
            # Similar for region, but allow it to be overridden.
            region = region if region else config.get('APP_AWS_REGION_NAME')
        return boto3.Session(
            aws_access_key_id=key_id, aws_secret_access_key=secret,
            region_name=region)
