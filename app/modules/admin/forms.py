# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import validators, IntegerField, BooleanField
from wtforms.widgets import HiddenInput

from app.modules.forms import NullStringField


class AdminJobForm(FlaskForm):
    job_id = IntegerField(
        validators=[validators.DataRequired()],
        widget=HiddenInput()
    )

    is_published = BooleanField(
        validators=[validators.DataRequired()],
        widget=HiddenInput(),
        default=False
    )

    hiring_company = NullStringField(
        label=u'Hiring Company',
        validators=[validators.Length(max=255)]
    )

    position_title = NullStringField(
        label=u'Position Title',
        validators=[validators.Length(max=255)]
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
        label=u'Active Facebook Bot URL',
        validators=[validators.Length(max=1024)]
    )

    active_fb_bot_id = IntegerField(
        label=u'Active Facebook Bot ID'
    )

    passive_fb_bot_url = NullStringField(
        label=u'Passive Facebook Bot URL',
        validators=[validators.Length(max=1024)]
    )

    passive_fb_bot_id = IntegerField(
        label=u'Passive Facebook Bot ID'
    )

    active_web_bot_url = NullStringField(
        label=u'Active Web Bot URL',
        validators=[validators.Length(max=1024)]
    )

    active_web_bot_id = IntegerField(
        label=u'Active Web Bot ID'
    )

    passive_web_bot_url = NullStringField(
        label=u'Passive Web Bot URL',
        validators=[validators.Length(max=1024)]
    )

    passive_web_bot_id = IntegerField(
        label=u'Passive Web Bot ID'
    )

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
