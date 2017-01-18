# -*- coding: utf-8 -*-
"""
    app.modules.errors
    ~~~~~~~~~~~~~~~~~~~~~

    Base errors
"""
from app.core import AppError


class AppInvalidTypeError(AppError):
    """Invalid type error class."""


class AppInvalidValueError(AppError):
    """Invalid value error class."""


class AppInvalidDateError(AppError):
    """Invalid date error class."""


class AppIllegalOperationError(AppError):
    """Illegal operation error class."""
