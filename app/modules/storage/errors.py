# -*- coding: utf-8 -*-
"""
    app.modules.storage.errors
    ~~~~~~~~~~~~~~~~~~~~~

    Storage module errors
"""
from app.modules.aws.errors import AppUploadFailedError


class AppUploadFailedFileExistsError(AppUploadFailedError):
    """A file upload failed because the file already exists."""
