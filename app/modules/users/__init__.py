# -*- coding: utf-8 -*-
"""
    app.modules.users
    ~~~~~~~~~~~~~~

    users module
"""
from flask_login import LoginManager
from flask_security import SQLAlchemyUserDatastore
from app.extensions import security, db
from .models import User, Role
from flask_wtf.csrf import CSRFProtect


def init_security(app, users_service):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.user_loader(users_service.get)

    # Don't use the default blueprints so we can perform social login.
    security.init_app(app, SQLAlchemyUserDatastore(db, User, Role))

    CSRFProtect(app)
