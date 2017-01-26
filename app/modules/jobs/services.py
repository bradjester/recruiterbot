# -*- coding: utf-8 -*-
"""
    app.modules.jobs.services
    ~~~~~~~~~~~~~~

    Jobs module services
"""
from flask import url_for

from app.core import Service
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
            .filter(Candidate.bot.job_id == job_id, Candidate.name is None)\
            .all()

    @staticmethod
    def find_candidates_by_job_id(job_id, company_id):
        return Candidate.query\
            .filter(Candidate.bot.job_id == job_id, company_id=company_id)\
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

    def __init__(self, static_storage_service):
        super(JobsService, self).__init__()
        self.static_storage_service = static_storage_service

    def get_jobs_data(self, company_id):
        jobs = self.find_all_by_company(company_id)
        return [self._get_job_data(j) for j in jobs]

    def _get_job_data(self, job):
        candidate_count = 0
        if job.jd_file_key is not None:
            jd_file_key = self.static_storage_service.generate_signed_url(
                job.jd_file_key)
        else:
            jd_file_key = None

        job_data = dict(
            id=job.id,
            title=job.title,
            is_published=job.is_published,
            jd_file_key=jd_file_key
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

    def find_by_uuid(self, uuid, company_id):
        return self.first(uuid=uuid, company_id=company_id)
