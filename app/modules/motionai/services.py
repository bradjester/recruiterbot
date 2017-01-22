# -*- coding: utf-8 -*-
"""
    app.modules.motionai.services
    ~~~~~~~~~~~~~~

    MotionAI module services
"""
from app.core import Service
from app.modules.motionai.models import Message


class WebhookService(Service):
    __model__ = Message
