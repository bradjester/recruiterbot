# -*- coding: utf-8 -*-
"""
    recruiterbot.modules.api.views
    ~~~~~~~~~~~~~~~~~~~~~

    API views
"""
from flask import Blueprint, jsonify, request
from flask_security import current_user

from app.helpers import route
from app.services import static_storage_service, candidates_service

api_bp = Blueprint('api', __name__, template_folder="templates",
                   url_prefix="/api")


@route(api_bp, '/job_description/<uuid>/signed-post/<filename>')
def get_job_description_signed_post(uuid, filename):
    content_type = request.args.get('content-type')
    # Always overwrite existing individual images.
    data = static_storage_service.generate_job_description_signed_post(
        uuid, filename, overwrite=True, content_type=content_type)
    return jsonify(data=data)


@route(api_bp, '/candidate/<int:candidate_id>', methods=['PUT'],
       endpoint='put_candidate')
def update_candidate(candidate_id):
    data = request.get_json()
    comp_id = current_user.company_id
    candidate = candidates_service.find_by_id_company(candidate_id, comp_id)
    if not candidate:
        return jsonify(error="No candidate found for id: {}".format(
            candidate_id)), 404
    candidates_service.update(candidate, **data)
    return '', 204
