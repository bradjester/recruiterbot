# -*- coding: utf-8 -*-
"""
    app.modules.motionai.services
    ~~~~~~~~~~~~~~

    MotionAI module services
"""
from app.core import Service
from app.modules.motionai.models import Message, Bot
from .models import Message


class WebhookService(Service):
    __model__ = Message


class BotsService(Service):
    __model__ = Bot

    def find_bot_by_motionai_botid(self, bot_id):
        return self.first(bot_id=bot_id)


class MessagesService(Service):
    __model__ = Message

    def get_sorted_messages_by_candidate_ids(self, candidate_list):
        model = self.__model__
        # Data is ordered by (candidate_id , received_at)
        return model.query.filter(
            model.candidate_id.in_(candidate_list)).orderby(model.candidate_id, model.received_at).all()

    def get_sorted_messages_by_candidate_id(self, candidate_id):
        model = self.__model__
        # Data is ordered by received_at
        return model.query.filter(
            model.candidate_id == candidate_id).orderby(model.received_at).all()
