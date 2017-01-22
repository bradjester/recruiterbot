"""
    app.modules.motionai.forms
    ~~~~~~~~~~~~~

    MotionAI forms module
"""

from flask_wtf import Form
from wtforms import validators, SelectField, BooleanField, DateField, \
    TextAreaField, DateTimeField, StringField, IntegerField

from app.modules.forms import NullStringField


class MotionAIWebhookForm(Form):
    received_at = DateTimeField(
        label='updated_at',
        validators=[validators.InputRequired()],
        format='%Y-%m-%dT%H:%M:%S.%fZ')
    sender = StringField(
        label='from',
        validators=[validators.InputRequired(), validators.Length(max=255)])
    receiver = StringField(
        label='to',
        validators=[validators.InputRequired(), validators.Length(max=255)])
    reply = StringField(
        label='reply',
        validators=[validators.InputRequired()])
    reply_data = NullStringField(
        label='replyData',
        validators=[validators.Optional()])
    bot_id = IntegerField(
        label='botID',
        validators=[validators.InputRequired()])
    module_id = IntegerField(
        label='moduleID',
        validators=[validators.InputRequired()])
    session = StringField(
        label='session',
        validators=[validators.InputRequired()])
    direction = StringField(
        label='direction',
        validators=[validators.InputRequired()])
    attached_media = StringField(
        label='attachedMedia',
        validators=[validators.Optional()])
