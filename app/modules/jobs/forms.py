# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import validators, HiddenField

from app.modules.forms import NullStringField


class JobForm(FlaskForm):
    title = NullStringField(
        label=u'Name',
        validators=[
            validators.InputRequired(),
            validators.Length(max=255)
        ]
    )
    jd_file_url = HiddenField(
        label=u'Job Description Key',
        validators=[validators.DataRequired(), validators.Length(max=1024)])
    uuid = HiddenField(
        label=u'UUID',
        validators=[validators.DataRequired(), validators.Length(max=36)])
