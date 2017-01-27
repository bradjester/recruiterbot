# -*- coding: utf-8 -*-
"""
    recruiterbot.modules.api.views
    ~~~~~~~~~~~~~~~~~~~~~

    API views
"""
from flask import Blueprint, jsonify, request

# from app.core import PHWMFormError, PHWMInvalidAttributeError
from app.helpers import route
from app.services import static_storage_service, candidates_service
from flask_security import current_user

api_bp = Blueprint('api', __name__, template_folder="templates",
                   url_prefix="/api")


@route(api_bp, '/job_description/<uuid>/signed-post/<filename>')
def get_job_description_signed_post(uuid, filename):
    content_type = request.args.get('content-type')
    # Always overwrite existing individual images.
    data = static_storage_service.generate_job_description_signed_post(
        uuid, filename, overwrite=True, content_type=content_type)
    return jsonify(data=data)


@route(api_bp, '/candidate/<int:candidate_id>/set_rating/<int:rating>')
def set_candidate_rating(candidate_id, rating):
    comp_id = current_user.company_id
    candidate = candidates_service.find_by_id_company(candidate_id, comp_id)
    if not candidate:
        return jsonify(error="No candidate found for id: {}".format(
            candidate_id)), 404
    candidate.rating = rating
    candidates_service.save(candidate)
    return jsonify(data="Rating updated")
