# -*- coding: utf-8 -*-
from app.modules.aws.services import AWSService, AWSS3Service, AWSSESService
from app.modules.storage.services import StaticStorageService
from app.modules.users.services import RolesService, UsersService

# User Services
roles_service = RolesService()
users_service = UsersService()

# AWS Services
aws_service = AWSService()
aws_s3_service = AWSS3Service(aws_service)
aws_ses_service = AWSSESService(aws_service)

# Static Storage Service
static_storage_service = StaticStorageService(aws_s3_service)
