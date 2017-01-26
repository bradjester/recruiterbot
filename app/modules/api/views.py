# -*- coding: utf-8 -*-
"""
    recruiterbot.modules.api.views
    ~~~~~~~~~~~~~~~~~~~~~

    API views
"""
from flask import Blueprint, jsonify, request

# from app.core import PHWMFormError, PHWMInvalidAttributeError
from app.helpers import route
from app.services import static_storage_service

api_bp = Blueprint('api', __name__, template_folder="templates",
                   url_prefix="/api")


@route(api_bp,
       '/job_description/<uuid>/signed-post/<filename>')
def get_job_description_signed_post(uuid, filename):
    content_type = request.args.get('content-type')
    # Always overwrite existing individual images.
    data = static_storage_service.generate_job_description_signed_post(
        uuid, filename, overwrite=True, content_type=content_type)
    return jsonify(data=data)
