# -*- coding: utf-8 -*-
"""
    app.modules.motionai.views
    ~~~~~~~~~~~~~~

    MotionAI module views
"""
from flask import Blueprint, render_template, request, url_for, redirect, \
    jsonify
from app.helpers import route
from .forms import MotionAIWebhookForm
from app.services import webhook_service
import logging

webhook_bp = Blueprint('webhook', __name__)


@webhook_bp.route('/webhook', methods=['POST'], endpoint='webhook')
def webhook_handler():
    if request.method == 'POST':
        form = MotionAIWebhookForm(request.form, csrf_enabled=False)
        if not form.validate():
            logging.error('Error while validating forms with the following data: {}'.format(str(request.form)))
            # Doesn't matter what we return, but necessary to log the error
            return jsonify({'message': 'Error while parsing form data'})
        message = webhook_service.new()
        _save_message(message, form)
        return jsonify({'message': 'Message Parsed Successfully'})
    else:
        return jsonify({'message': 'GET Request not allowed'})


def _save_message(message, form):
    form.populate_obj(message)
    webhook_service.save(message, commit=True)
