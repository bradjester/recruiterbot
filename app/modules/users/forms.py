# -*- coding: utf-8 -*-
"""
    app.modules.users.forms
    ~~~~~~~~~~~~~~~~~~~~~

    User forms
"""
from flask.ext.security import RegisterForm
from wtforms import StringField
from wtforms import validators


class ExtendedRegisterForm(RegisterForm):
    name = StringField(
        label=u'Name',
        validators=[
            validators.DataRequired(),
            validators.Length(max=255)
        ]
    )
