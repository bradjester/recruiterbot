# -*- coding: utf-8 -*-
from app.core import Service
from .models import Job


class JobsService(Service):
    __model__ = Job

    def get_jobs_data(self, company_id):
        jobs = self.find_all_by_company(company_id)
        return [self._get_job_data(j) for j in jobs]

    @staticmethod
    def _get_job_data(job):
        candidate_count = 0
        job_data = dict(id=job.id, title=job.title)
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
