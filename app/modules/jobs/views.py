# -*- coding: utf-8 -*-
import uuid

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user

from app.helpers import route
from app.modules.jobs.forms import JobForm
from app.services import jobs_service

job_bp = Blueprint('job', __name__, template_folder="templates",
                   url_prefix="/jobs")


@route(job_bp, '/', methods=['GET', 'POST'], endpoint='index')
def job_index():
    cur_company = current_user.company

    if request.method == 'POST':
        form = JobForm(request.form)
        if not form.validate():
            return _show_job_new_template(form), 400

        job = jobs_service.new()
        form.populate_obj(job)

        # Generate a UUID for the job and set company to current before save.
        job.uuid = uuid.uuid4()
        job.company = cur_company
        jobs_service.save(job)

        # Redirect to GET to prevent a form resubmission on refresh
        return redirect(url_for("job.index"))

    jobs_data = []
    if cur_company:
        jobs_data = jobs_service.get_jobs_data(cur_company.id)

    return render_template('jobs/job_index.html', jobs=jobs_data)


@route(job_bp, '/new', endpoint='new')
def job_new():
    form = JobForm(company=current_user.company.id)
    return _show_job_new_template(form)


def _show_job_new_template(form):
    return render_template("jobs/job_new.html", form=form)


@route(job_bp, '/<int:id>', methods=['PUT'], endpoint='update')
def job_update(id):
    cur_company = current_user.company
    job = jobs_service.find_by_id_company(id, cur_company.id)

    form = JobForm(request.form)

    if not form.validate():
        return _show_job_edit_template(form, job), 400

    form.populate_obj(job)
    jobs_service.save(job)

    return redirect(url_for('job.index', id=job.id))


@route(job_bp, '/<int:id>/edit', endpoint='edit')
def job_edit(id):
    job = jobs_service.find_by_id_company(id, current_user.company.id)
    form = JobForm(obj=job)
    return _show_job_edit_template(form, job)


def _show_job_edit_template(form, job):
    return render_template("jobs/job_edit.html", form=form, job_id=job.id)