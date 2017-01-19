# -*- coding: utf-8 -*-
"""
    app.modules.motionai.models
    ~~~~~~~~~~~~~~~~~~~~~

    MotionAI module models
"""
from app.extensions import db
from app.modules.base import Base
from sqlalchemy.dialects.mysql import DATETIME


class Bot(Base):
    __tablename__ = 'bots'

    bot_id = db.Column(db.BigInteger, unique=True)  # To be extracted from the bot's url params
    bot_url = db.Column(db.String(1024))

    job_id = db.Column(
        db.Integer,
        db.ForeignKey('jobs.id', name='bot_job_fk',
                      onupdate='CASCADE', ondelete='CASCADE'))  # If a job gets deleted - delete all corresponding  bots

    job = db.relationship("Job")

    channel_type = db.Column(db.String(255))
    chat_type = db.Column(db.String(255))

    def __str__(self):
        return 'Bot : {}'.format(self.bot_id)


class Message(Base):
    __tablename__ = 'messages'

    received_at = db.Column(DATETIME(fsp=3))  # millisecond precision
    sender = db.Column(db.String(255))
    receiver = db.Column(db.String(255))
    reply = db.Column(db.String(4095))  # Max message length ? Suggestion to increase
    reply_data = db.Column(db.String(1024))  # 1024 chars should be enough for parsed fields
    job_id = db.Column(
        db.Integer,
        db.ForeignKey('jobs.id', name='message_job_fk',
                      onupdate='CASCADE', ondelete='CASCADE'))  # If a job gets deleted - delete all corresponding msgs

    bot_id = db.Column(
        db.BigInteger,
        db.ForeignKey('bots.bot_id', name='message_bot_fk',
                      onupdate='CASCADE', ondelete='CASCADE'))  # If a bot gets deleted - delete all corresponding msgs

    bot = db.relationship(
        "Bot",
        foreign_keys=bot_id)

    module_id = db.Column(db.Integer)
    session_id = db.Column(db.String(1024))
    direction = db.Column(db.String(3))  # Should be `in` or `out`
    attached_media = db.Column(db.String(1024))
    secret = db.Column(db.String(1024))

    def __str__(self):
        return 'Message: {}'.format(self.reply)
