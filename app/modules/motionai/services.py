# -*- coding: utf-8 -*-
"""
    app.modules.motionai.services
    ~~~~~~~~~~~~~~

    MotionAI module services
"""
from app.core import Service
from app.modules.motionai.models import Message, Bot
from .models import Message
from .errors import MotionAISecretKeyMismatch
from datetime import datetime
from flask import current_app


class WebhookService(Service):
    __model__ = Message

    def __init__(self, bots_service, candidates_service):
        super(WebhookService, self).__init__()
        self.bots_service = bots_service
        self.candidates_service = candidates_service

    def create_message(self, data_dict):
        if data_dict['secret'] != current_app.config.get('WEBHOOK_SECRET_KEY'):
            raise MotionAISecretKeyMismatch

        bot_id = data_dict['botID']
        bot = self.bots_service.find_bot_by_motionai_bot_id(bot_id)

        session_id = data_dict['session']
        candidate = self.candidates_service.find_candidate_by_session_id(session_id)

        if candidate is None:
            # Create candidate with existing session_id
            candidate = self.candidates_service.create(bot_id=bot.id, session_id=session_id,
                                                       company_id=bot.job.company_id, commit=False)
        # optional fields
        if 'replyData' not in data_dict:
            data_dict['replyData'] = None
        if 'attachedMedia' not in data_dict:
            data_dict['attachedMedia'] = None

        msg = self.create(
            secret=data_dict.get('secret'),
            received_at=datetime.strptime(data_dict.get('updatedAt'), "%Y-%m-%dT%H:%M:%S.%fZ"),
            bot_id=bot_id,
            bot=bot,
            candidate_id=candidate.id,
            candidate=candidate,
            sender=data_dict.get('from'),
            receiver=data_dict.get('to'),
            reply=data_dict.get('reply'),
            reply_data=data_dict.get('replyData'),
            module_id=data_dict.get('moduleID'),
            direction=data_dict.get('direction'),
            company_id=bot.job.company_id)
        return msg


class BotsService(Service):
    __model__ = Bot

    def find_bot_by_motionai_bot_id(self, bot_id):
        return self.first(bot_id=bot_id)


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
