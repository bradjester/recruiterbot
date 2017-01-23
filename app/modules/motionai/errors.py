# -*- coding: utf-8 -*-
"""
    app.modules.users.errors
    ~~~~~~~~~~~~~~~~~~~~~

    User errors
"""
from app.core import AppError


class MotionAISecretKeyMismatch(AppError):
    """The secret key received from MotionAI does not match the key set on this application"""
