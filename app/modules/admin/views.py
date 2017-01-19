# -*- coding: utf-8 -*-
"""
    app.modules.admin.views
    ~~~~~~~~~~~~~~~~~~~~~

    Admin views
"""
from datetime import datetime

from flask_admin import AdminIndexView
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import typefmt as sqla_typefmt
from flask_admin.model import typefmt
from flask_security import current_user

from app.extensions import db
from app.helpers import format_datetime
from app.models import User, Role


class AdminBlocker(object):
    @staticmethod
    def is_accessible():
        if current_user.is_authenticated and current_user.is_admin:
            return True
        return False


def null_formatter(view, value):
    return typefmt.empty_formatter(view, value)


def datetime_format(view, date):
    # Remove unused parameter.
    del view

    return format_datetime(date)


def user_format(view, user):
    # Remove unused parameter.
    del view

    return user.get_display_name(include_id=True, include_email=True)


DEFAULT_FORMATTERS = dict(sqla_typefmt.DEFAULT_FORMATTERS)
DEFAULT_FORMATTERS.update({
    type(None): null_formatter,
    datetime: datetime_format,
    User: user_format
})


class AppAdminIndexView(AdminBlocker, AdminIndexView):
    pass


class UserModelView(AdminBlocker, sqla.ModelView):
    def __init__(self):
        super(UserModelView, self).__init__(User, db.session, name=u'Users')

    can_delete = False
    can_create = False
    column_display_pk = True

    column_type_formatters = DEFAULT_FORMATTERS

    column_list = (
        User.id.name,
        User.first_name.name,
        User.surname.name,
        User.email.name,
        User.active.name,
        User.roles.key,
        User.login_count.name,
        User.current_login_at.name,
        User.last_login_at.name,
        User.current_login_ip.name,
        User.last_login_ip.name,
        User.created_at.name,
        User.updated_at.name
    )

    column_labels = dict(
        first_name=u'Given Name',
        surname=u'Surname',
        current_login_at=u'Login Timestamp',
        last_login_at=u'Last Login Timestamp',
        created_at=u'Created Timestamp',
        updated_at=u'Updated Timestamp'
    )

    form_columns = (
        User.first_name.name,
        User.surname.name,
        User.active.name,
        User.roles.key
    )

    form_excluded_columns = (
        User.confirmed_at.name,
        User.email.name,
        User.login_count.name,
        User.current_login_at.name,
        User.last_login_at.name,
        User.current_login_ip.name,
        User.last_login_ip.name,
        User.created_at.name,
        User.updated_at.name
    )

    # Only show users with the social login type in the admin view.
    def get_query(self):
        return super(UserModelView, self).get_query()

    def get_count_query(self):
        return super(UserModelView, self).get_count_query()


class RoleModelView(AdminBlocker, sqla.ModelView):
    def __init__(self):
        super(RoleModelView, self).__init__(
            Role, db.session, name=u'Roles')

    can_delete = False
    can_create = False
    can_edit = False

    column_type_formatters = DEFAULT_FORMATTERS

    column_list = (
        Role.name.name,
        Role.description.name,
        Role.created_at.name,
        Role.updated_at.name
    )

    column_labels = dict(
        created_at=u'Created Timestamp',
        updated_at=u'Updated Timestamp'
    )
