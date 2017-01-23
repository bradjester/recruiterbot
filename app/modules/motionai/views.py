# -*- coding: utf-8 -*-
"""
    app.modules.motionai.views
    ~~~~~~~~~~~~~~

    MotionAI module views
"""
from flask import Blueprint, render_template, request, url_for, redirect, \
    jsonify

from .helpers import webhook_dict_to_model, dict_from_form
from app.services import webhook_service
import logging

webhook_bp = Blueprint('webhook', __name__)


@webhook_bp.route('/webhook', methods=['GET', 'POST'])
def webhook_handler():
    if request.method == 'POST':
        message_dict = dict_from_form(request.form)
        message_obj = webhook_dict_to_model(message_dict)

        if message_obj is None:
            logging.error("MotionAI Secret Key Mismatch")
            return jsonify({'message': 'Secret Key did not match'})

        webhook_service.save(message_obj, commit=True)

        # The responses don't matter
        return jsonify({'message': 'Message Parsed Successfully and saved to DB'})
    else:
        return jsonify({'message': 'GET Request not allowed'})
