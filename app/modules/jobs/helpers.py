# -*- coding: utf-8 -*-
"""
    app.modules.jobs.helpers
    ~~~~~~~~~~~~~~~~~~~~~

    Jobs module helpers
"""


def get_candidate_id_to_msgs(message_list):
    candidate_messages = {}
    for message in message_list:
        if not message.id in candidate_messages.keys():
            candidate_messages[message.candidate_id] = [message]
        else:
            candidate_messages[message.candidate_id].append(message)

    return candidate_messages
