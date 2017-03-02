# -*- coding: utf-8 -*-
"""
    app.modules.daxtra.errors
    ~~~~~~~~~~~~~~~~~~~~~

    Daxtra errors
"""
from app.core import AppError


class DaxtraResponseIdNotFound(AppError):
    """Expected CandidateId/VacancyId from Daxtra Response but not found"""


class DaxtraResponseResultNotFound(AppError):
    """Expected Result with score from Daxtra Response but not found"""


class DaxtraResponseStatusNotOkay(AppError):
    """Expected Status Code 100  "OK" from Daxtra Response but not received"""
