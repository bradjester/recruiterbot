# -*- coding: utf-8 -*-
"""
    app.modules.jobs.models
    ~~~~~~~~~~~~~~~~~~~~~

    Jobs module models
"""
import sqlalchemy as sa

from app.extensions import db
from app.modules.base import Base


class Job(Base):
    __tablename__ = 'jobs'

    company_id = db.Column(
        db.Integer,
        db.ForeignKey('companies.id', name='job_company_fk'))

    company = db.relationship(
        "Company",
        single_parent=True,
        foreign_keys=company_id)

    title = db.Column(db.String(255))
    is_published = db.Column(db.Boolean, server_default=sa.text("'0'"), default=False)
    uuid = db.Column(db.String(11))  # youtube uses 11 char url uuids as well; keyspace : [0-9A-Za-z_-]
    jd_file_url = db.Column(db.String(1024))

    @property
    def display_title(self):
        return self.get_display_title()

    def get_display_title(self, include_id=False, include_uuid=False):
        title = self.title
        if include_id:
            title = u'{}: {}'.format(self.id, title)
        if include_uuid:
            title = u'{} <{}>'.format(title, self.uuid)
        return title

    def __str__(self):
        return self.title


class Candidate(Base):
    __tablename__ = 'candidates'

    name = db.Column(db.String(255))

    job_id = db.Column(
        db.Integer,
        db.ForeignKey('jobs.id', name='candidate_job_fk'))

    job = db.relationship(
        "Job",
        single_parent=True,  # one candidate record -> one job record, because we're using session_id for identification
        foreign_keys=job_id)

    # bot_id = db.Column(
    #     db.Integer,
    #     db.ForeignKey('bots.id', name='cand_bot_fk'))
    #
    # bot = db.relationship(
    #     "Bot",
    #     single_parent=True,
    #     foreign_keys=bot_id)

    resume_url = db.Column(db.String(1024))

    # # Suggestion Required: Don't know if the following will work properly
    # session_id = db.Column(
    #     db.String(1024),
    #     db.ForeignKey('messages.session_id', name='session_session_fk'))

    @property
    def display_name(self):
        return self.get_display_name()

    def get_display_name(self, include_id=False, include_job=False):
        name = self.name
        if include_id:
            name = u'{}: {}'.format(self.id, name)
        if include_job:
            name = u'{} <{}>'.format(name, self.job.name)
        return name

    def __str__(self):
        return self.name
