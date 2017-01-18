# -*- coding: utf-8 -*-
"""
    app.modules.users.errors
    ~~~~~~~~~~~~~~~~~~~~~

    User errors
"""
from app.core import AppError


class AppEmailInvalidError(AppError):
    """Wrong email format"""
