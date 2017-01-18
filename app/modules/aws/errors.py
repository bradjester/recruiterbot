# -*- coding: utf-8 -*-
"""
    app.modules.aws.errors
    ~~~~~~~~~~~~~~~~~~~~~

    AWS module errors
"""
from app.core import AppError


class AppUploadFailedError(AppError):
    """An error occurred during a file upload."""
