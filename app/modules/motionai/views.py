# -*- coding: utf-8 -*-
"""
    app.modules.motionai.views
    ~~~~~~~~~~~~~~

    MotionAI module views
"""
from flask import Blueprint, request, jsonify
from .errors import MotionAISecretKeyMismatch
from app.services import webhook_service
from app.services import jobs_service
import logging

webhook_bp = Blueprint('webhook', __name__)


@webhook_bp.route('/webhook', methods=['POST'])
def webhook_handler():
    if request.method == 'POST':
        message_dict = request.form.to_dict()
        try:
            msg = webhook_service.create_message(message_dict)
        except MotionAISecretKeyMismatch:
            logging.error("MotionAI Secret Key Mismatch")
            return jsonify({'message': 'Secret Key did not match'})

        # These custom variables can be used by MotionAI Modules for creating customized messages and building urls
        return '', 200
    else:
        return '', 405


@webhook_bp.route('/webhook/<string:session_id>', methods=['GET'])
def get_job_uuid_from_session_id(session_id):
    if request.method == 'GET':
        job = jobs_service.get_by_session_id(session_id)

        if job is None:
            logging.error("Job UUID not found for session : {}".format(session_id))
            return '', 204
        else:
            return jsonify({'job_uuid': job.uuid}), 200
    else:
        return '', 405
