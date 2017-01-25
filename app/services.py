# -*- coding: utf-8 -*-
from app.modules.aws.services import AWSService, AWSS3Service, AWSSESService
from app.modules.jobs.services import CandidatesService, JobsService
from app.modules.motionai.services import WebhookService, BotsService, \
    MessagesService
from app.modules.storage.services import StaticStorageService
from app.modules.users.services import RolesService, UsersService, \
    CompaniesService

# User Services
roles_service = RolesService()
users_service = UsersService()
companies_service = CompaniesService()

# Job Services
jobs_service = JobsService()

# AWS Services
aws_service = AWSService()
aws_s3_service = AWSS3Service(aws_service)
aws_ses_service = AWSSESService(aws_service)

# Static Storage Service
static_storage_service = StaticStorageService(aws_s3_service)

# Bots Service
bots_service = BotsService()

# Messages Service
messages_service = MessagesService()

# Candidates Service
candidates_service = CandidatesService(messages_service)

# MotionAI Webhook Service
webhook_service = WebhookService(bots_service, candidates_service)
