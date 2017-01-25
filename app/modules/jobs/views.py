
# -*- coding: utf-8 -*-
"""
    app.modules.jobs.views
    ~~~~~~~~~~~~~

    views module for the frontend
"""
from flask import Blueprint, render_template
from app.services import jobs_service, candidates_service, messages_service
from flask_login import current_user

candidates_bp = Blueprint('candidates', __name__, template_folder="templates", url_prefix='/candidates')


@candidates_bp.route('/<string:job_uuid>', methods=['GET'], endpoint='index')
def job_candidates_index(job_uuid,):
    job = jobs_service.find_job_by_uuid(job_uuid, current_user.company_id)
    candidates_service.update_candidates_with_no_name(job.id)
    candidates = candidates_service.find_candidates_by_jobid(job.id, current_user.company_id)
    return render_template('candidates/candidates.html', candidates=candidates)


@candidates_bp.route('/<int:candidate_id>/', methods=['GET'], endpoint='show')
def candidate_with_messages_show(candidate_id):
    candidate = candidates_service.find_by_id_company(candidate_id, current_user.company_id)
    messages = messages_service.get_sorted_messages_by_candidate_id(candidate_id, current_user.company_id)
    # Could possible convert messages into json ({message.received_at : message}) rather than a list of messages
    return render_template('candidate/candidate_show.html', candidate=candidate, messages=messages)
