# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import validators, IntegerField, BooleanField, HiddenField, \
    StringField
from wtforms.widgets import HiddenInput, TextArea

from app.modules.forms import NullStringField


class AdminJobForm(FlaskForm):
    job_id = IntegerField(
        validators=[validators.DataRequired()],
        widget=HiddenInput()
    )

    title = HiddenField(
        label=u'Name',
        validators=[
            validators.Length(max=255)
        ]
    )

    is_published = BooleanField(
        label="Publish",
        default=False
    )

    hiring_company = NullStringField(
        label=u'Hiring Company',
        validators=[validators.Length(max=255), validators.DataRequired()]
    )

    position_title = NullStringField(
        label=u'Position Title',
        validators=[validators.Length(max=255), validators.DataRequired()]
    )

    location = NullStringField(
        label=u'Location',
        validators=[validators.Length(max=255)]
    )

    work_type = NullStringField(
        label=u'Work Type',
        validators=[validators.Length(max=255)]
    )

    expected_salary = NullStringField(
        label=u'Expected Salary',
        validators=[validators.Length(max=255)]
    )

    active_fb_bot_url = NullStringField(
        label=u'FB URL',
        validators=[validators.Length(max=1024)]
    )

    active_fb_bot_id = IntegerField(
        label=u'FB ID',
        validators=[validators.optional()],
    )

    passive_fb_bot_url = NullStringField(
        label=u'FB URL',
        validators=[validators.Length(max=1024)]
    )

    passive_fb_bot_id = IntegerField(
        label=u'FB ID',
        validators=[validators.optional()],
    )

    active_web_bot_url = NullStringField(
        label=u'Web URL',
        validators=[validators.Length(max=1024)]
    )

    active_web_bot_id = IntegerField(
        label=u'Web ID',
        validators=[validators.optional()],
    )

    passive_web_bot_url = NullStringField(
        label=u'Web URL',
        validators=[validators.Length(max=1024)]
    )

    passive_web_bot_id = IntegerField(
        label=u'Web ID',
        validators=[validators.optional()],
    )

    banner_file_key = HiddenField(
        label=u'Banner Key',
        validators=[validators.Length(max=1024)])

    uuid = HiddenField(
        label=u'UUID',
        validators=[validators.DataRequired(), validators.Length(max=36)])

    description = StringField(
        label=u'Description', widget=TextArea())

    def validate(self):
        valid = FlaskForm.validate(self)

        if self.active_fb_bot_id.data and not self.active_fb_bot_url.data:
            self.active_fb_bot_url.errors.append(
                'URL must be included with Bot ID')
            valid = False

        if self.active_fb_bot_url.data and not self.active_fb_bot_id.data:
            self.active_fb_bot_id.errors.append(
                'Bot ID must be included with URL')
            valid = False

        if self.passive_fb_bot_id.data and not self.passive_fb_bot_url.data:
            self.passive_fb_bot_url.errors.append(
                'URL must be included with Bot ID')
            valid = False

        if self.passive_fb_bot_url.data and not self.passive_fb_bot_id.data:
            self.passive_fb_bot_id.errors.append(
                'Bot ID must be included with URL')
            valid = False

        if self.active_web_bot_id.data and not self.active_web_bot_url.data:
            self.active_web_bot_url.errors.append(
                'URL must be included with Bot ID')
            valid = False

        if self.active_web_bot_url.data and not self.active_web_bot_id.data:
            self.active_web_bot_id.errors.append(
                'Bot ID must be included with URL')
            valid = False

        if self.passive_web_bot_id.data and not self.passive_web_bot_url.data:
            self.passive_web_bot_url.errors.append(
                'URL must be included with Bot ID')
            valid = False

        if self.passive_web_bot_url.data and not self.passive_web_bot_id.data:
            self.passive_web_bot_id.errors.append(
                'Bot ID must be included with URL')
            valid = False

        return valid
