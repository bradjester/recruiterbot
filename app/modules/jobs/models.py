# -*- coding: utf-8 -*-
"""
    app.modules.jobs.models
    ~~~~~~~~~~~~~~~~~~~~~

    Jobs module models
"""
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from app.extensions import db
from app.modules.base import Base


class Job(Base):
    __tablename__ = 'jobs'

    company_id = db.Column(
        db.Integer,
        db.ForeignKey('companies.id', name='job_company_fk',
                      onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False)

    company = db.relationship(
        "Company",
        foreign_keys=company_id,
    )

    title = db.Column(db.String(255), nullable=False)
    hiring_company = db.Column(db.String(255))
    location = db.Column(db.String(255))
    work_type = db.Column(db.String(255))
    expected_salary = db.Column(db.String(255))
    description = db.Column(mysql.MEDIUMTEXT)
    is_published = db.Column(
        db.Boolean,
        server_default=sa.text("'0'"),
        default=False,
        nullable=False
    )
    uuid = db.Column(db.String(36), unique=True, nullable=False)
    jd_file_url = db.Column(db.String(1024))


class Candidate(Base):
    __tablename__ = 'candidates'

    bot_id = db.Column(
        db.Integer,
        db.ForeignKey('bots.id', name='candidate_bot_fk',
                      onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False)

    bot = db.relationship(
        "Bot",
        foreign_keys=bot_id,
        backref=db.backref(
            'candidates',
            lazy='dynamic',
            cascade="all, delete-orphan"
        )
    )

    company_id = db.Column(
        db.Integer,
        db.ForeignKey('companies.id', name='candidate_company_fk',
                      onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False)

    company = db.relationship(
        "Company",
        foreign_keys=company_id,
    )

    name = db.Column(db.String(255))
    resume_url = db.Column(db.String(1024))
    session_id = db.Column(db.String(1024), nullable=False)
    status = db.Column(db.String(255), default="New", nullable=False)
    rating = db.Column(db.Integer())
