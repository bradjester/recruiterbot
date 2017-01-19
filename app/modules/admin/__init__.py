# -*- coding: utf-8 -*-
"""
    app.modules.admin
    ~~~~~~~~~~~~~~~~~~

    admin module
"""
from flask_admin import Admin
from flask_admin.base import MenuLink

from .views import AppAdminIndexView, UserModelView, RoleModelView


def init_admin(app):
    admin = Admin(app, name=u'Admin', template_mode='bootstrap3',
                  index_view=AppAdminIndexView())
    admin.add_view(UserModelView())
    admin.add_view(RoleModelView())
    admin.add_link(MenuLink(name='Back to Main Site', url='/'))
