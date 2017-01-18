# -*- coding: utf-8 -*-
"""
    app.modules.users.services
    ~~~~~~~~~~~~~~~~~~~~~

    User services
"""
from app.core import Service
from .models import User, Role


class RolesService(Service):
    __model__ = Role


class UsersService(Service):
    __model__ = User
