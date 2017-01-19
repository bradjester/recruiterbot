# -*- coding: utf-8 -*-
"""
    app.modules.motionai.constants
    ~~~~~~~~~~~~~~

    MotionAI module constants
"""

valid_channel_types = ['fb', 'web']
valid_chat_types = ['active', 'passive']

# The fields below refer to the fields in json received from Motion AI's Webhook REST API
valid_webhook_fields = ['updated_at', 'from', 'to', 'reply', 'replyData', 'botID', 'moduleID',
                        'session', 'direction', 'attachedMedia', 'secret']

valid_directions = ['in', 'out']