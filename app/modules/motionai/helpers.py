# -*- coding: utf-8 -*-
"""
    app.modules.motionai.helpers
    ~~~~~~~~~~~~~~~~~~~~~

    MotionAI module helpers
"""
from .models import Message
from app.modules.jobs.models import Candidate
from app.services import candidates_service, bots_service
from .constants import WEBHOOK_SECRET_KEY
from .errors import MotionAISecretKeyMismatch
from datetime import datetime


def webhook_dict_to_model(data_dict):
    if data_dict['secret'] != WEBHOOK_SECRET_KEY:
        raise MotionAISecretKeyMismatch
        return None

    msg = Message()
    msg.secret = data_dict['secret']
    msg.received_at = datetime.strptime(data_dict['updatedAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
    msg.sender = data_dict['from']
    msg.receiver = data_dict['to']
    msg.module_id = data_dict['moduleID']
    msg.reply = data_dict['reply']
    msg.direction = data_dict['direction']

    bot_id = data_dict['botID']
    bot = bots_service.find_bot_by_motionai_botid(bot_id)

    if bot is not None:
        msg.bot_id = bot.id
        msg.bot = bot

    session_id = data_dict['session']
    candidate = candidates_service.find_candidate_by_sessionid(session_id)

    if candidate is not None:
        msg.candidate_id = candidate.id
        msg.candidate = candidate
    else:
        # Create candidate with existing session_id
        new_candidate = Candidate(bot_id=msg.bot_id, session_id=session_id)
        msg.candidate = candidates_service.save(new_candidate,commit=True)
        msg.candidate_id = msg.candidate.id

    # optional fields
    if 'replyData' in data_dict.keys():
        msg.reply_data = data_dict['replyData']
    if 'attachedMedia' in data_dict.keys():
        msg.attached_media_url = data_dict['attachedMedia']

    return msg


def dict_from_form(form):
    data_dict = {}
    data_dict['secret'] = form.getlist('secret')[0]
    data_dict['updatedAt'] = form.getlist('updatedAt')[0]
    data_dict['from'] = form.getlist('from')[0]
    data_dict['to'] = form.getlist('to')[0]
    data_dict['direction'] = form.getlist('direction')[0]
    data_dict['botID'] = form.getlist('botID')[0]
    data_dict['moduleID'] = form.getlist('moduleID')[0]
    data_dict['reply'] = form.getlist('reply')[0]
    data_dict['session'] = form.getlist('session')[0]
    data_dict['updatedAt'] = form.getlist('updatedAt')[0]

    if len(form.getlist('replydata')) > 0:
        data_dict['replyData'] =  form.getlist('replydata')[0]
    if len(form.getlist('attachedMedia')) > 0:
        data_dict['attachedMedia'] = form.getlist('attachedMedia')[0]
    return data_dict
