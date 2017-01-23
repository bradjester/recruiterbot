# -*- coding: utf-8 -*-
"""
    app.modules.users.services
    ~~~~~~~~~~~~~~~~~~~~~

    User services
"""
from app.core import Service
from .models import User, Role, Company


class RolesService(Service):
    __model__ = Role


class UsersService(Service):
    __model__ = User


class CompaniesService(Service):
    __model__ = Company

    def find_company_by_title(self, title):
        return self.first(title=title)
