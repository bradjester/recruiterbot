# -*- coding: utf-8 -*-
"""
    app.modules.motionai.views
    ~~~~~~~~~~~~~~

    MotionAI module views
"""
import logging

from flask import Blueprint, request, jsonify

from app.services import jobs_service
from app.services import webhook_service
from .errors import MotionAISecretKeyMismatch

webhook_bp = Blueprint('webhook', __name__)


@webhook_bp.route('/webhook', methods=['POST'])
def webhook_handler():
    message_dict = request.form.to_dict()
    try:
        webhook_service.create_message(message_dict)
    except MotionAISecretKeyMismatch:
        logging.error("MotionAI Secret Key Mismatch")
        return jsonify({'message': 'Secret Key did not match'}), 401

    return '', 200


@webhook_bp.route('/webhook/<string:session_id>', methods=['GET'])
def get_job_uuid_from_session_id(session_id):
    job = jobs_service.get_by_session_id(session_id)

    if job is None:
        logging.error("Job UUID not found for session: {}".format(session_id))
        return '', 204

    return jsonify({'job_uuid': job.uuid}), 200
