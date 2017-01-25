# -*- coding: utf-8 -*-
"""
    app.modules.jobs.views
    ~~~~~~~~~~~~~

    views module for the frontend
"""
import uuid

from flask import Blueprint, render_template
from flask import redirect
from flask import request
from flask import url_for
from flask_login import current_user

from app.helpers import route
from app.modules.jobs.forms import JobForm
from app.services import jobs_service, candidates_service, messages_service

candidates_bp = Blueprint('candidates', __name__, template_folder="templates",
                          url_prefix='/candidates')


@candidates_bp.route('/<string:job_uuid>', methods=['GET'], endpoint='index')
def job_candidates_index(job_uuid,):
    job = jobs_service.find_job_by_uuid(job_uuid, current_user.company_id)
    candidates_service.update_candidates_with_no_name(job.id)
    candidates = candidates_service.find_candidates_by_jobid(
        job.id, current_user.company_id)
    return render_template('candidates/candidates.html', candidates=candidates)


@candidates_bp.route('/<int:candidate_id>/', methods=['GET'], endpoint='show')
def candidate_with_messages_show(candidate_id):
    candidate = candidates_service.find_by_id_company(
        candidate_id, current_user.company_id)
    messages = messages_service.get_sorted_messages_by_candidate_id(
        candidate_id, current_user.company_id)
    # Could possible convert messages into json
    # ({message.received_at : message}) rather than a list of messages
    return render_template('candidate/candidate_show.html',
                           candidate=candidate, messages=messages)


job_bp = Blueprint('job', __name__, template_folder="templates",
                   url_prefix="/jobs")


@route(job_bp, '/', methods=['GET', 'POST'], endpoint='index')
def job_index():
    if request.method == 'POST':
        form = JobForm(request.form)
        if not form.validate():
            return _show_job_new_template(form), 400

        job = jobs_service.new()
        form.populate_obj(job)

        # Generate a UUID for the job and set company to current before save.
        job.uuid = uuid.uuid4()
        job.company = current_user.company
        jobs_service.save(job)

        # Redirect to GET to prevent a form resubmission on refresh
        return redirect(url_for("job.index"))

    jobs_data = jobs_service.get_jobs_data(current_user.company_id)

    return render_template('jobs/job_index.html', jobs=jobs_data,
                           company=cur_company)


@route(job_bp, '/new', endpoint='new')
def job_new():
    form = JobForm(company=current_user.company.id)
    return _show_job_new_template(form)


def _show_job_new_template(form):
    return render_template("jobs/job_new.html", form=form)


@route(job_bp, '/<int:id>', methods=['PUT'], endpoint='update')
def job_update(id):
    job = jobs_service.find_by_id_company(id, current_user.company_id)

    form = JobForm(request.form)

    if not form.validate():
        return _show_job_edit_template(form, job), 400

    form.populate_obj(job)
    jobs_service.save(job)

    return redirect(url_for('job.index', id=job.id))


@route(job_bp, '/<int:id>/edit', endpoint='edit')
def job_edit(id):
    job = jobs_service.find_by_id_company(id, current_user.company_id)
    form = JobForm(obj=job)
    return _show_job_edit_template(form, job)


def _show_job_edit_template(form, job):
    return render_template("jobs/job_edit.html", form=form, job_id=job.id)
