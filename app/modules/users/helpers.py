# -*- coding: utf-8 -*-
"""
    app.modules.users.helpers
    ~~~~~~~~~~~~~~~~~~~~~

    User helpers
"""
import logging

from .errors import AppEmailInvalidError


def check_email_validity(email):
    logger = logging.getLogger(__name__)
    if "@" not in email:
        msg = u"{} is not a valid email format.".format(email)
        logger.warning(msg)
        raise AppEmailInvalidError(msg)
