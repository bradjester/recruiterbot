
# -*- coding: utf-8 -*-
"""
    phwm.modules.frontend.views
    ~~~~~~~~~~~~~

    views module for the frontend
"""
from flask import Blueprint, render_template
from app.services import jobs_service, candidates_service, messages_service
candidates_bp = Blueprint('candidates', __name__, template_folder="templates", url_prefix='/candidates')


@candidates_bp.route('/<string:job_uuid>',methods=['GET'], endpoint='index')
def candidates_show(job_uuid):
    job = jobs_service.find_job_by_uuid(job_uuid)

    # Fetch candidates with no name by job id, get all messages for these candidates, extract name from messages,
    # update candidates with no names, retrieve all candidates and return
    candidates_noname = candidates_service.find_noname_candidates_by_jobid(job.id)
    candidate_ids = [x.id for x in candidates_noname]
    messages = messages_service.get_sorted_messages_by_candidate_ids(candidate_ids)
    candidates_service.update_candidates_with_no_name(candidates_noname, messages)
    candidates = candidates_service.find_candidates_by_jobid(job.id)
    return render_template('candidates/candidates.html', candidates=candidates)

#
# @candidates_bp.route('/<int:candidate_id>/', methods=['GET'], endpoint='show')
# def candidate_with_messages_show(candidate_id):
#     candidate = candidates_service.first(id=candidate_id)
#     messages = messages_service.get_sorted_messages_by_candidate_id(candidate_id)
#     # Could possible convert messages into json ({message.received_at : message}) rather than a list of messages
#     return render_template('candidate/candidate_show.html', candidate=candidate, messages=messages)
