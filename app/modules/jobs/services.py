# -*- coding: utf-8 -*-
"""
    app.modules.jobs.services
    ~~~~~~~~~~~~~~

    Jobs module services
"""
from app.core import Service
from app.modules.jobs.models import Candidate, Job
from app.modules.motionai.models import Bot
from .helpers import get_candidateid_to_msgs_dict


class CandidatesService(Service):
    __model__ = Candidate

    def find_candidate_by_sessionid(self, session_id):
        return self.first(session_id=session_id)

    # When this service is triggered, we should try and populate the name of the candidate from the application
    # Logic : filter candidates by job, for each candidate query the messages_table
    #   Search for string What is your full name?

    def find_noname_candidates_by_jobid(self, job_id):
        model = self.__model__
        # Filtering candidates by name == NULL and job_id
        return model.query.join(Bot, model.bot_id == Bot.id).filter(Bot.job_id == job_id, model.name is None).all()

    def find_candidates_by_jobid(self, job_id):
        model = self.__model__
        return model.query.join(Bot, model.bot_id == Bot.id).filter(Bot.job_id == job_id).all()

    def update_candidates_with_no_name(self, noname_candidates, messages):
        # Dictionary of candidate.id : candidate
        candidate_id_to_candidate = dict([(x.id, x) for x in noname_candidates])
        # grouping messages like this : {candidate_id : [messages for candidate]}
        candidate_id_to_messages_dict = get_candidateid_to_msgs_dict(messages)

        for candidate_id in candidate_id_to_messages_dict .keys():
            next_message_is_name = False
            for message in candidate_id_to_messages_dict [candidate_id]:
                if message.reply == 'What is your full name?':
                    next_message_is_name = True
                    continue
                if next_message_is_name:
                    candidate_id_to_candidate[candidate_id].name = message.reply

        candidate_with_names = list(candidate_id_to_candidate.values())

        # Write a service to bulk update candidates?
        for candidate in candidate_with_names:
            self.update(candidate, commit=True)


class JobsService(Service):
    __model__ = Job

    def find_jobs_by_companyid(self, company_id):
        model = self.__model__
        return model.query.filter(model.company_id == company_id).all()

    def find_job_by_uuid(self, uuid):
        model = self.__model__
        return self.first(uuid=uuid)
