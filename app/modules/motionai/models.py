# -*- coding: utf-8 -*-
"""
    app.modules.motionai.models
    ~~~~~~~~~~~~~~~~~~~~~

    MotionAI module models
"""
from app.extensions import db
from app.modules.base import Base
from sqlalchemy.dialects.mysql import DATETIME, TEXT


class Bot(Base):
    __tablename__ = 'bots'

    job_id = db.Column(
        db.Integer,
        db.ForeignKey('jobs.id', name='bot_job_fk',
                      onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False)

    job = db.relationship(
        "Job",
        foreign_keys=job_id,
    )

    company_id = db.Column(
        db.Integer,
        db.ForeignKey('companies.id', name='bot_company_fk',
                      onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False)

    company = db.relationship(
        "Company",
        foreign_keys=company_id)

    bot_id = db.Column(db.BigInteger, unique=True, nullable=False)
    bot_url = db.Column(db.String(1024), nullable=False)
    channel_type = db.Column(db.String(255), nullable=False)
    chat_type = db.Column(db.String(255), nullable=False)


class Message(Base):
    __tablename__ = 'messages'

    bot_id = db.Column(
        db.BigInteger,
        db.ForeignKey('bots.bot_id', name='message_bot_fk',
                      onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False)

    bot = db.relationship(
        "Bot",
        foreign_keys=bot_id,
        backref=db.backref(
            'bots',
            lazy='dynamic',
            cascade="all, delete-orphan"
        )
    )

    candidate_id = db.Column(
        db.Integer,
        db.ForeignKey('candidates.id', name='message_candidate_fk',
                      onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False)

    candidate = db.relationship(
        "Candidate",
        foreign_keys=candidate_id,
        backref=db.backref(
            'candidate',
            lazy='dynamic',
            cascade="all, delete-orphan"
        )
    )

    company_id = db.Column(
        db.Integer,
        db.ForeignKey('companies.id', name='message_company_fk',
                      onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False)

    company = db.relationship(
        "Company",
        foreign_keys=company_id)

    received_at = db.Column(DATETIME(fsp=3), nullable=False)
    sender = db.Column(db.String(255), nullable=False)
    receiver = db.Column(db.String(255), nullable=False)
    reply = db.Column(TEXT, nullable=False)
    reply_data = db.Column(db.String(1024))
    module_id = db.Column(db.Integer, nullable=False)
    direction = db.Column(db.String(3), nullable=False)
    attached_media_url = db.Column(db.String(1024))
    secret = db.Column(db.String(1024), nullable=False)
