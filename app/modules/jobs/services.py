# -*- coding: utf-8 -*-
"""
    app.modules.jobs.services
    ~~~~~~~~~~~~~~

    Jobs module services
"""
from app.core import Service
from app.modules.motionai.models import Bot
from .helpers import get_candidate_id_to_msgs
from .models import Candidate, Job


class CandidatesService(Service):
    __model__ = Candidate

    def __init__(self, messages_service):
        super(CandidatesService, self).__init__()
        self.messages_service = messages_service

    def find_candidate_by_session_id(self, session_id):
        return self.first(session_id=session_id)

    def find_by_id_company(self, _id, company_id):
        return self.first(id=_id, company_id=company_id)

    @staticmethod
    def _find_no_name_candidates_by_job_id(job_id):
        # Filtering candidates by name == NULL and job_id
        return Candidate.query\
            .filter(Bot.job_id == job_id, Candidate.name is None)\
            .join(Bot, Bot.id == Candidate.bot_id)\
            .all()

    @staticmethod
    def find_candidates_by_job_id(job_id, company_id):
        return Candidate.query\
            .filter(Bot.job_id == job_id, Candidate.company_id == company_id)\
            .join(Bot, Bot.id == Candidate.bot_id)\
            .all()

    def update_candidates_with_no_name(self, job_id):
        unnamed_candidates = self._find_no_name_candidates_by_job_id(job_id)
        # Dictionary of candidate.id : candidate
        candidate_id_to_candidate = {x.id: x for x in unnamed_candidates}

        messages = self.messages_service.get_sorted_messages_by_candidate_ids(
            candidate_id_to_candidate.keys())

        # grouping messages like this:
        # {candidate_id : [messages for candidate]}
        candidate_id_to_messages = get_candidate_id_to_msgs(messages)

        named_candidates = []
        for candidate_id in candidate_id_to_messages:
            next_message_is_name = False
            for message in candidate_id_to_messages[candidate_id]:
                if message.reply == 'What is your full name?':
                    next_message_is_name = True
                    continue
                if next_message_is_name:
                    candidate_id_to_candidate[candidate_id].name = \
                        message.reply
                    named_candidates.append(
                        candidate_id_to_candidate[candidate_id])
                    break

        self.save_all(named_candidates)


class JobsService(Service):
    __model__ = Job

    def __init__(self, candidates_service):
        super(JobsService, self).__init__()
        self.candidates_service = candidates_service

    def get_jobs_data(self, company_id):
        jobs = self.find_all_by_company(company_id)
        return [self._get_job_data(j) for j in jobs]

    @staticmethod
    def _get_job_data(job):
        candidate_count = 0
        job_data = dict(
            id=job.id,
            title=job.title,
            is_published=job.is_published,
            jd_file_key=job.jd_file_key,
            uuid=job.uuid
        )
        for bot in job.bots:
            candidate_count += bot.candidates.count()
            url_key = bot.channel_type + '_' + bot.chat_type + '_url'
            job_data[url_key] = bot.bot_url
        job_data['candidate_count'] = candidate_count
        return job_data

    def find_by_id_company(self, _id, company_id):
        return self.first(id=_id, company_id=company_id)

    def find_all_by_company(self, company_id):
        return self.find_all(company_id=company_id)

    def find_by_uuid(self, uuid):
        return self.first(uuid=uuid)

    def get_by_session_id(self, session_id):
        candidate = self.candidates_service.find_candidate_by_session_id(
            session_id)
        return candidate.bot.job if candidate else None

