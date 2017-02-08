# -*- coding: utf-8 -*-
"""
    app.modules.jobs.helpers
    ~~~~~~~~~~~~~~~~~~~~~

    Jobs module helpers
"""
import re


def get_candidate_id_to_msgs(message_list):
    candidate_messages = {}
    for message in message_list:
        if message.candidate_id not in candidate_messages.keys():
            candidate_messages[message.candidate_id] = [message]
        else:
            candidate_messages[message.candidate_id].append(message)

    return candidate_messages


# Process messages by handling special situations like a ::next:: block or
# a responseTo block.
def process_messages(messages):
    processed = []
    module_reply_map = {}
    for message in messages:
        reply = message.reply
        direction = message.direction
        attached_media_url = message.attached_media_url
        if attached_media_url:
            processed.append(dict(
                reply=reply,
                direction=direction,
                attached_media_url=attached_media_url,
            ))
            continue

        subreplies = reply.split("::next::")
        for subreply in subreplies:
            processed_subreply = _process_subreply(subreply, module_reply_map)
            processed.append(dict(
                reply=processed_subreply,
                direction=direction,
            ))

        if message.module_id:
            if message.module_id not in module_reply_map:
                module_reply_map[message.module_id] = [reply]
            else:
                module_reply_map[message.module_id].append(reply)

    return processed


# Assume responseTo is always the first item in a bracketed area.
RESPONSE_TO_PREFIX_REGEX = re.compile('\[responseTo')

# Assume module id always ends on either a space or a bracket.
MODULE_ID_REGEX = re.compile('module=[^\s\]]*')

# Assume fallback always ends on a bracket.
FALLBACK_TEXT_REGEX = re.compile('fallback=[^\]]*')


# Process a subreply by looking for and processing a responseTo block, if any.
def _process_subreply(reply, module_reply_map):
    resp_to_result = RESPONSE_TO_PREFIX_REGEX.search(reply)
    if resp_to_result:
        start_resp_to = resp_to_result.start()
        end_resp_to = start_resp_to
        bracket_count = 0
        # Can't use a regex to extract because there could be nested
        # brackets in the fallback message.
        for i, char in enumerate(reply[start_resp_to:]):
            if char == '[':
                bracket_count += 1
            elif char == ']':
                bracket_count -= 1
                if bracket_count == 0:
                    end_resp_to = i + start_resp_to + 1
                    break

        resp_to = reply[start_resp_to:end_resp_to]
        if resp_to:
            repl_text = _get_replace_text_from_response_to(
                resp_to, module_reply_map
            )
            reply = reply[0:start_resp_to] + repl_text + reply[end_resp_to:]

    return reply


# Get the text we should replace in a message from a responseTo block.
# We try to replace with text from a module, but use fallback if the module
# doesn't exist.
def _get_replace_text_from_response_to(resp_to, module_reply_map):
    if not resp_to:
        return ''

    repl_text = ''
    module_id_res = MODULE_ID_REGEX.search(resp_to)
    if module_id_res:
        module_id = module_id_res.group().split("=")[1]
        module_msgs = module_reply_map.get(module_id)
        if module_msgs:
            repl_text = module_msgs[-1]
    if not repl_text:
        fallback_res = FALLBACK_TEXT_REGEX.search(resp_to)
        if fallback_res:
            repl_text = fallback_res.group().split("=")[1]

    return repl_text
