# -*- coding: utf-8 -*-
"""
    app.modules.motionai.services
    ~~~~~~~~~~~~~~

    MotionAI module services
"""
from datetime import datetime

from flask import current_app

from app.core import Service
from app.modules.motionai.models import Bot
from .errors import MotionAISecretKeyMismatch
from .models import Message


class WebhookService(Service):
    __model__ = Message

    def __init__(self, bots_service, candidates_service, messages_service):
        super(WebhookService, self).__init__()
        self.bots_service = bots_service
        self.candidates_service = candidates_service
        self.messages_service = messages_service

    def create_message(self, data_dict):
        if data_dict['secret'] != current_app.config.get('WEBHOOK_SECRET_KEY'):
            raise MotionAISecretKeyMismatch

        bot = self.bots_service.find_bot_by_motionai_bot_id(
            data_dict.get('botID'))

        session_id = data_dict.get('session')
        candidate = self.candidates_service.find_candidate_by_session_id(
            session_id)

        if candidate is None:
            # Create candidate with existing session_id
            candidate = self.candidates_service.create(
                bot_id=bot.id,
                session_id=session_id,
                company_id=bot.job.company_id,
                commit=False
            )

        return self.create_message_from_data(
            bot,
            candidate,
            bot.job.company,
            data_dict,
        )

    def create_message_from_data(self, bot, candidate, company, data,
                                 commit=True):
        return self.messages_service.create(
            bot=bot,
            company=company,
            candidate=candidate,
            received_at=datetime.strptime(data.get('updatedAt'),
                                          "%Y-%m-%dT%H:%M:%S.%fZ"),
            sender=data.get('from'),
            receiver=data.get('to'),
            reply=data.get('reply'),
            reply_data=data.get('replyData'),
            module_id=data.get('moduleID'),
            direction=data.get('direction'),
            attached_media_url=data.get('attachedMedia'),
            commit=commit,
        )


class BotsService(Service):
    __model__ = Bot

    def find_bot_by_motionai_bot_id(self, bot_id):
        return self.first(bot_id=bot_id)

    def find_all_for_job(self, job_id):
        return self.find_all(job_id=job_id)


class MessagesService(Service):
    __model__ = Message

    @staticmethod
    def get_sorted_messages_by_candidate_ids(candidate_list):
        # Data is ordered by (candidate_id , received_at)
        return Message.query\
            .filter(Message.candidate_id.in_(candidate_list))\
            .order_by(Message.candidate_id, Message.received_at)\
            .all()

    @staticmethod
    def get_sorted_messages_by_candidate_id(candidate_id, company_id):
        # Data is ordered by received_at
        return Message.query\
            .filter_by(candidate_id=candidate_id, company_id=company_id)\
            .order_by(Message.received_at)\
            .all()
