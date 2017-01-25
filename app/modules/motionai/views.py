# -*- coding: utf-8 -*-
"""
    app.modules.motionai.views
    ~~~~~~~~~~~~~~

    MotionAI module views
"""
from flask import Blueprint, request, jsonify
from .errors import MotionAISecretKeyMismatch
from app.services import webhook_service
import logging

webhook_bp = Blueprint('webhook', __name__)


@webhook_bp.route('/webhook', methods=['POST'])
def webhook_handler():
    if request.method == 'POST':
        message_dict = request.form.to_dict()
        try:
            webhook_service.create_message(message_dict)
        except MotionAISecretKeyMismatch:
            logging.error("MotionAI Secret Key Mismatch")
            return jsonify({'message': 'Secret Key did not match'})
        return '', 200
    else:
        return '', 405