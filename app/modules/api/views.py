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


@route(api_bp, '/jobs/<job_uuid>/descriptions/signed-post/<filename>',
       endpoint='get_job_description_signed_post')
def get_job_description_signed_post(job_uuid, filename):
    content_type = request.args.get('content-type')
    data = static_storage_service.generate_job_description_signed_post(
        job_uuid, filename, overwrite=True, content_type=content_type)
    return jsonify(data=data)


# This route is intentionally insecure.
@api_bp.route('/jobs/<job_uuid>/candidates/<session_id>/resumes'
              '/signed-post/<filename>',
              endpoint='get_job_candidate_resume_signed_post')
def get_job_candidate_resume_signed_post(job_uuid, session_id, filename):
    candidate = candidates_service.find_candidate_by_session_id(session_id)
    if not candidate:
        return jsonify(error="No candidate associated with session id: {}".
                       format(session_id)), 404
    if candidate.bot.job.uuid != job_uuid:
        return jsonify(error="Candidate not associated with this job"), 404

    content_type = request.args.get('content-type')
    data = static_storage_service.generate_job_candidate_resume_signed_post(
        job_uuid, session_id, filename, overwrite=True,
        content_type=content_type)
    return jsonify(data=data)


@route(api_bp, '/image/<uuid>/signed-post/<filename>')
def get_image_signed_post(uuid, filename):
    content_type = request.args.get('content-type')
    # Always overwrite existing individual images.
    data = static_storage_service.generate_job_image_signed_post(
        uuid, filename, overwrite=True, content_type=content_type)
    return jsonify(data=data)


@api_bp.route('/candidate/resume_key',
              methods=['PUT'], endpoint='put_candidate_key')
def update_candidate_key():
    data = request.get_json()
    candidate = candidates_service.find_candidate_by_session_id(
        data['session_id'])
    if not candidate:
        return jsonify(error="No candidate associated with session id: {}".
                       format(data.session_id)), 404
    if candidate.bot.job.uuid != data['job_uuid']:
        return jsonify(error="Candidate not associated with this job"), 404

    candidates_service.update(candidate, resume_key=data['resume_key'])
    return '', 204


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
