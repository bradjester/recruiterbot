# -*- coding: utf-8 -*-
"""
    app.modules.admin.views
    ~~~~~~~~~~~~~~~~~~~~~

    Admin views
"""
from datetime import datetime

from flask import redirect
from flask import request
from flask import url_for
from flask_admin import expose
from flask_admin import AdminIndexView
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import typefmt as sqla_typefmt
from flask_admin.model import typefmt
from flask_security import current_user
from markupsafe import Markup
from sqlalchemy import func

from app.extensions import db
from app.helpers import format_datetime, utc_now
from app.models import User, Role
from app.modules.admin.forms import AdminJobForm
from app.modules.jobs.models import Job, Candidate
from app.modules.motionai.constants import BOT_FB_CHAN_TYPE, \
    BOT_ACTIVE_CHAT_TYPE, BOT_PASSIVE_CHAT_TYPE, BOT_WEB_CHAN_TYPE
from app.modules.motionai.models import Bot
from app.modules.users.models import Company
from app.services import jobs_service, bots_service


class AdminBlocker(object):
    @staticmethod
    def is_accessible():
        if current_user.is_authenticated and current_user.is_admin:
            return True
        return False


def null_formatter(view, value):
    return typefmt.empty_formatter(view, value)


def datetime_format(view, date):
    # Remove unused parameter.
    del view

    return format_datetime(date)


def user_format(view, user):
    # Remove unused parameter.
    del view

    return user.get_display_name(include_id=True, include_email=True)


DEFAULT_FORMATTERS = dict(sqla_typefmt.DEFAULT_FORMATTERS)
DEFAULT_FORMATTERS.update({
    type(None): null_formatter,
    datetime: datetime_format,
    User: user_format
})


class AppAdminIndexView(AdminBlocker, AdminIndexView):
    def is_visible(self):
        return False
    

class UserModelView(AdminBlocker, sqla.ModelView):
    def __init__(self):
        super(UserModelView, self).__init__(User, db.session, name=u'Users')

    can_delete = False
    can_create = False
    column_display_pk = True

    column_type_formatters = DEFAULT_FORMATTERS

    column_list = (
        User.id.name,
        User.name.name,
        User.email.name,
        User.active.name,
        User.roles.key,
        User.company.key,
        User.login_count.name,
        User.current_login_at.name,
        User.last_login_at.name,
        User.current_login_ip.name,
        User.last_login_ip.name,
        User.created_at.name,
        User.updated_at.name
    )

    column_labels = dict(
        name=u'Name',
        current_login_at=u'Login Timestamp',
        last_login_at=u'Last Login Timestamp',
        created_at=u'Created Timestamp',
        updated_at=u'Updated Timestamp'
    )

    form_columns = (
        User.name.name,
        User.active.name,
        User.roles.key,
        User.company.key,
    )

    form_excluded_columns = (
        User.confirmed_at.name,
        User.email.name,
        User.login_count.name,
        User.current_login_at.name,
        User.last_login_at.name,
        User.current_login_ip.name,
        User.last_login_ip.name,
        User.created_at.name,
        User.updated_at.name,
    )

    # Only show users with the social login type in the admin view.
    def get_query(self):
        return super(UserModelView, self).get_query()

    def get_count_query(self):
        return super(UserModelView, self).get_count_query()


class RoleModelView(AdminBlocker, sqla.ModelView):
    def __init__(self):
        super(RoleModelView, self).__init__(
            Role, db.session, name=u'Roles')

    can_delete = False
    can_create = False
    can_edit = False

    column_type_formatters = DEFAULT_FORMATTERS

    column_list = (
        Role.name.name,
        Role.description.name,
        Role.created_at.name,
        Role.updated_at.name
    )

    column_labels = dict(
        created_at=u'Created Timestamp',
        updated_at=u'Updated Timestamp'
    )


class CompanyModelView(AdminBlocker, sqla.ModelView):
    def __init__(self):
        super(CompanyModelView, self).__init__(
            Company, db.session, name=u'Companies')

    can_delete = False
    can_create = True
    can_edit = True

    column_type_formatters = DEFAULT_FORMATTERS

    column_list = (
        Company.name.name,
        Company.created_at.name,
        Company.updated_at.name,
    )

    column_labels = dict(
        created_at=u'Created Timestamp',
        updated_at=u'Updated Timestamp'
    )

    form_columns = (
        Company.name.name,
    )

    form_excluded_columns = (
        Company.created_at.name,
        Company.updated_at.name,
    )


class JobModelView(AdminBlocker, sqla.ModelView):
    def __init__(self):
        super(JobModelView, self).__init__(
            Job, db.session, name=u'Jobs', endpoint='job_admin')

    can_delete = False
    can_create = False
    can_edit = True

    def _title_formatter(view, context, model, name):
        return Markup(
            '<a href="%s" target="_blank">%s</a>' % (
                url_for('job.show', job_uuid=model.uuid),
                model.title
            )
        )

    column_formatters = dict(
        title=_title_formatter
    )
    column_type_formatters = DEFAULT_FORMATTERS

    column_list = (
        "company_name",
        "candidate_count",
        "title",
    )

    def get_query(self):
        return (
            self.session.query(
                Job.id.label("id"),
                Job.title.label("title"),
                Job.uuid.label("uuid"),
                Company.name.label("company_name"),
                func.count(Candidate.id).label("candidate_count"),
            )
            .join(Company, Company.id == Job.company_id)
            .join(Bot, Bot.job_id == Job.id, isouter=True)
            .join(Candidate, Candidate.bot_id == Bot.id, isouter=True)
            .group_by(Job.id)
        )

    @expose('/edit/', methods=['GET', 'PUT'])
    def edit_job(self):
        job = jobs_service.get_or_404(request.args.get('id'))
        if request.method == 'PUT':
            form = AdminJobForm(request.form)

            if not form.validate():
                return self._show_job_edit_template(form, job.id), 400

            self._save_job_and_bots_from_form(form, job)

            # Redirect to GET to prevent a form resubmission on refresh
            return redirect(url_for("job_admin.index_view"))

        bots = bots_service.find_all_for_job(job.id)

        form = AdminJobForm()
        form.job_id.data = job.id
        form.is_published.data = job.is_published
        form.hiring_company.data = job.hiring_company
        form.position_title.data = job.position_title
        form.location.data = job.location
        form.work_type.data = job.work_type
        form.expected_salary.data = job.expected_salary
        form.title.data = job.title
        form.banner_file_key.data = job.banner_file_key
        form.uuid.data = job.uuid
        form.description.data = job.description

        for bot in bots:
            if bot.channel_type == BOT_FB_CHAN_TYPE:
                if bot.chat_type == BOT_ACTIVE_CHAT_TYPE:
                    form.active_fb_bot_pk.data = bot.id
                    form.active_fb_bot_url.data = bot.bot_url
                    form.active_fb_bot_id.data = bot.bot_id
                if bot.chat_type == BOT_PASSIVE_CHAT_TYPE:
                    form.passive_fb_bot_pk.data = bot.id
                    form.passive_fb_bot_url.data = bot.bot_url
                    form.passive_fb_bot_id.data = bot.bot_id
            if bot.channel_type == BOT_WEB_CHAN_TYPE:
                if bot.chat_type == BOT_ACTIVE_CHAT_TYPE:
                    form.active_web_bot_pk.data = bot.id
                    form.active_web_bot_url.data = bot.bot_url
                    form.active_web_bot_id.data = bot.bot_id
                if bot.chat_type == BOT_PASSIVE_CHAT_TYPE:
                    form.passive_web_bot_pk.data = bot.id
                    form.passive_web_bot_url.data = bot.bot_url
                    form.passive_web_bot_id.data = bot.bot_id

        return self._show_job_edit_template(form, job.id)

    def _show_job_edit_template(self, form, job_id):
        return self.render("/admin/job_edit.html", form=form, job_id=job_id)

    @staticmethod
    def _save_job_and_bots_from_form(form, job, commit=True):
        JobModelView._create_or_update_bots_from_form(form, job, commit=False)

        if form.is_published.data and not job.is_published:
            # If the job wasn't published and is now, then set time.
            job.published_at = utc_now()

        job.is_published = form.is_published.data
        job.hiring_company = form.hiring_company.data
        job.position_title = form.position_title.data
        job.location = form.location.data
        job.work_type = form.work_type.data
        job.expected_salary = form.expected_salary.data
        job.banner_file_key = form.banner_file_key.data
        job.description = form.description.data
        jobs_service.save(job, commit=commit)

    @staticmethod
    def _create_or_update_bots_from_form(form, job, commit=True):
        if form.active_fb_bot_id.data and form.active_fb_bot_url.data:
            bots_service.create_or_update(
                job.id,
                job.company_id,
                BOT_FB_CHAN_TYPE,
                BOT_ACTIVE_CHAT_TYPE,
                bot_id=form.active_fb_bot_id.data,
                bot_url=form.active_fb_bot_url.data,
                commit=commit,
            )

        if form.passive_fb_bot_id.data and form.passive_fb_bot_url.data:
            bots_service.create_or_update(
                job.id,
                job.company_id,
                BOT_FB_CHAN_TYPE,
                BOT_PASSIVE_CHAT_TYPE,
                bot_id=form.passive_fb_bot_id.data,
                bot_url=form.passive_fb_bot_url.data,
                commit=commit,
            )

        if form.active_web_bot_id.data and form.active_web_bot_url.data:
            bots_service.create_or_update(
                job.id,
                job.company_id,
                BOT_WEB_CHAN_TYPE,
                BOT_ACTIVE_CHAT_TYPE,
                bot_id=form.active_web_bot_id.data,
                bot_url=form.active_web_bot_url.data,
                commit=commit,
            )

        if form.passive_web_bot_id.data and form.passive_web_bot_url.data:
            bots_service.create_or_update(
                job.id,
                job.company_id,
                BOT_WEB_CHAN_TYPE,
                BOT_PASSIVE_CHAT_TYPE,
                bot_id=form.passive_web_bot_id.data,
                bot_url=form.passive_web_bot_url.data,
                commit=commit,
            )