# -*- coding: utf-8 -*-
"""
    app.modules.jobs.helpers
    ~~~~~~~~~~~~~~~~~~~~~

    Jobs module helpers
"""


def get_candidateid_to_msgs_dict(message_list):
    candidate_messages = {}
    for message in message_list:
        if not message.id in candidate_messages.keys():
            candidate_messages[message.id] = [message]
        else:
            candidate_messages[message.id].append(message)

    return candidate_messages
