# -*- coding: utf-8 -*-
"""
    app.modules.email
    ~~~~~~~~~~~~~~~~~~~~~

    Email utility
"""

from flask_mail import Message
from flask import current_app, render_template

from app.services import aws_ses_service


def send_mail(subject, recipients, template_folder, template, **context):
    """Send an email via the Flask-Mail extension.

    :param subject: Email subject
    :param recipients: Email recipients
    :param template_folder: The folder where templates are located
    :param template: The name of the email template
    :param context: The context to render the template with
    """

    if not isinstance(recipients, list):
        recipients = [recipients]

    msg = Message(subject,
                  sender=current_app.config.get('SECURITY_EMAIL_SENDER'),
                  recipients=recipients)

    ctx = (template_folder, template)
    msg.body = render_template('%s/%s.txt' % ctx, **context)
    msg.html = render_template('%s/%s.html' % ctx, **context)

    aws_ses_service.send_message(msg)
