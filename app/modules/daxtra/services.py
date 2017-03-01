# -*- coding: utf-8 -*-
from app.core import Service
from app.modules.daxtra.models import DaxtraVacancy, DaxtraCandidate


class DaxtraVacanciesService(Service):
    __model__ = DaxtraVacancy

    def __init__(self, static_storage_service):
        super().__init__()
        self.static_storage_service = static_storage_service

    def create_from_job(self, job):
        url = self.static_storage_service.generate_signed_url(job.jd_file_key)
        pass

    def update_from_job(self, job):
        pass


class DaxtraCandidatesService(Service):
    __model__ = DaxtraCandidate

    def __init__(self, static_storage_service):
        super().__init__()
        self.static_storage_service = static_storage_service

    def create_from_candidate(self, candidate):
        url = self.static_storage_service.generate_signed_url(
            candidate.resume_key
        )
        pass

    def update_from_candidate(self, candidate):
        pass

    def update_score(self, daxtra_candidate):
        pass
