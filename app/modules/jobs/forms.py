# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import validators

from app.modules.forms import NullStringField


class JobForm(FlaskForm):
    title = NullStringField(
        label=u'Name',
        validators=[
            validators.InputRequired(),
            validators.Length(max=255)
        ]
    )
