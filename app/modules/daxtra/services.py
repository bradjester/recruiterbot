# -*- coding: utf-8 -*-
import logging
from xml.etree.ElementTree import SubElement

import requests

from app.core import Service
from app.extensions import db
from app.modules.daxtra.models import DaxtraVacancy, DaxtraCandidate
from .helpers import  get_base_daxtra_request_xml, base_64_encode_document,\
    send_req_and_get_response_dict
from .constants import ADD_CANDIDATE_ACTION, ADD_VACANCY_ACTION, \
    UPDATE_CANDIDATE_ACTION, UPDATE_VACANCY_ACTION, \
    MATCH_CANDIDATE_ACTION, OK_STATUS


class DaxtraVacanciesService(Service):
    __model__ = DaxtraVacancy

    def __init__(self, static_storage_service, daxtra_candidates_service):
        super().__init__()
        self.static_storage_service = static_storage_service
        self.daxtra_candidates_service = daxtra_candidates_service

    def create_from_job(self, job):
        url = self.static_storage_service.generate_signed_url(job.jd_file_key)

        daxtra_id = self._create_daxtra_vacancy_and_get_id(url)

        return self.create(
            job=job,
            daxtra_id=daxtra_id
        )

    def update_from_job(self, job):
        url = self.static_storage_service.generate_signed_url(job.jd_file_key)
        daxtra_vacancy = self.find(job_id=job.id)
        ret_daxtra_id = self._update_daxtra_vacancy_and_get_id(url)

        # Set the daxtra scores for this job.id to null
        if daxtra_vacancy.daxtra_id == ret_daxtra_id:  # all went well
            self.daxtra_candidates_service.set_scores_to_null_for_daxtra_vacancy_id(  # noqa
                daxtra_vacancy.daxtra_id
            )

    def _create_daxtra_vacancy_and_get_id(self, file_url):
        dx_request = get_base_daxtra_request_xml(ADD_VACANCY_ACTION)

        vacancy = SubElement(dx_request, 'Vacancy')

        vacancy_jd = SubElement(vacancy, 'Profile')
        vacancy_jd.text = base_64_encode_document(file_url)

        response_dict = send_req_and_get_response_dict(dx_request)

        return self._get_vacancy_id_from_response(response_dict,
                                                  ADD_VACANCY_ACTION)

    def _update_daxtra_vacancy_and_get_id(self, daxtra_id, file_url):
        dx_request = get_base_daxtra_request_xml(UPDATE_VACANCY_ACTION)

        vacancy = SubElement(dx_request, 'Vacancy')

        vacancy_id = SubElement(vacancy, 'VacancyId')
        vacancy_id.text = daxtra_id

        vacancy_jd = SubElement(vacancy, 'Profile')
        vacancy_jd.text = base_64_encode_document(file_url)

        response_dict = send_req_and_get_response_dict(dx_request)

        return self._get_vacancy_id_from_response(response_dict,
                                                  UPDATE_VACANCY_ACTION)

    @staticmethod
    def _get_vacancy_id_from_response(response_dict, action_type):
        # API Response format docs :
        # https://es-demo.daxtra.com/webservices/docs/add_vacancy.html
        # https://es-demo.daxtra.com/webservices/docs/update_vacancy.html

        status_code = response_dict.get('DxResponse').get('Status').get('Code')
        vacancy_id = response_dict.get('DxResponse').get('Vacancy').get(
            'VacancyId')
        if status_code and status_code == OK_STATUS:
            if vacancy_id:
                return vacancy_id
            else:
                logging.error('[{}] No Vacancy ID in Daxtra Response'.format(
                    action_type))
        else:
            logging.error('[{}] Return Not Okay Status : {}'.format(
                action_type,
                response_dict.get('DxResponse').get('Status')))


class DaxtraCandidatesService(Service):
    __model__ = DaxtraCandidate

    def __init__(self, static_storage_service):
        super().__init__()
        self.static_storage_service = static_storage_service

    def create_from_candidate(self, candidate):
        url = self.static_storage_service.generate_signed_url(
            candidate.resume_key)

        daxtra_id = self._create_daxtra_candidate_and_get_id(url)

        daxtra_vacancy = candidate.bot.job.daxtra_vacancy

        return self.create(
            daxtra_vacancy=daxtra_vacancy,
            candidate=candidate,
            daxtra_id=daxtra_id
        )

    def _create_daxtra_candidate_and_get_id(self, file_url):
        dx_request = get_base_daxtra_request_xml(ADD_CANDIDATE_ACTION)

        vacancy = SubElement(dx_request, 'Candidate')

        vacancy_jd = SubElement(vacancy, 'Profile')
        vacancy_jd.text = base_64_encode_document(file_url)

        response_dict = send_req_and_get_response_dict(dx_request)

        return self._get_candidate_id_from_response(response_dict,
                                                    ADD_CANDIDATE_ACTION)

    def update_from_candidate(self, candidate):
        url = self.static_storage_service.generate_signed_url(
            candidate.resume_key)

        daxtra_candidate = self.find(candidate_id=candidate.id)

        ret_daxtra_id = self._update_daxtra_candidate_and_get_id(url)

        # Set the daxtra scores for this candidate.id to null
        if daxtra_candidate.daxtra_id == ret_daxtra_id:  # all went well
            daxtra_candidate.score = None
            self.save(daxtra_candidate)
        else:
            logging.error('Error while updating candidate with id {} on daxtra'
                          ' db. Id returned from daxtra is not the same.')

    def _update_daxtra_candidate_and_get_id(self, daxtra_id, file_url):
        dx_request = get_base_daxtra_request_xml(UPDATE_CANDIDATE_ACTION)

        vacancy = SubElement(dx_request, 'Vacancy')

        vacancy_id = SubElement(vacancy, 'VacancyId')
        vacancy_id.text = daxtra_id

        vacancy_jd = SubElement(vacancy, 'Profile')
        vacancy_jd.text = base_64_encode_document(file_url)

        response_dict = send_req_and_get_response_dict(dx_request)

        return self._get_candidate_id_from_response(response_dict,
                                                    UPDATE_CANDIDATE_ACTION)

    def update_missing_scores(self, job_id):
        daxtra_candidates = DaxtraCandidate.query\
            .join(
                DaxtraVacancy,
                DaxtraCandidate.daxtra_vacancy_id == DaxtraVacancy.id
            ).filter(
                DaxtraVacancy.job_id == job_id,
                DaxtraCandidate.score is None
            )
        for daxtra_candidate in daxtra_candidates:
            self.update_score(daxtra_candidate, commit=False)
        db.session.commit()

    def update_score(self, daxtra_candidate, commit=True):
        self._fetch_daxtra_score_for_candidate(daxtra_candidate)
        return self.save(daxtra_candidate, commit=commit)

    def _fetch_daxtra_score_for_candidate(self, daxtra_candidate):
        dx_request = get_base_daxtra_request_xml(
            MATCH_CANDIDATE_ACTION,
            options='details'
        )
        daxtra_vacancy = daxtra_candidate.daxtra_vacancy

        candidate_elem = SubElement(dx_request, 'Candidate')

        dx_candidate_id = SubElement(candidate_elem, 'CandidateId')
        dx_candidate_id = daxtra_candidate.daxtra_id

        vacancy = SubElement(dx_request, 'Vacancy')

        structured_options = SubElement(vacancy, 'StructuredOptions')

        dx_vacancy_id = SubElement(structured_options, 'VacancyId')
        dx_vacancy_id.text = daxtra_vacancy

        response_dict = send_req_and_get_response_dict(dx_request)

        return self._get_score_from_response(response_dict)

    @staticmethod
    def _get_score_from_response(response_dict):
        # API Response format docs :
        # https://es-demo.daxtra.com/webservices/docs/match_candidate.html

        status_code = response_dict.get('DxResponse').get('Status').get('Code')
        result = response_dict.get('DxResponse').get('Results').get('Result')

        if status_code and status_code == OK_STATUS:
            if result:
                return float(result.get('DxResponse').get(
                    'Results').get('Result').get('Score'))
            else:
                logging.error('[match_candidate] No Result in Daxtra Response')
        else:
            logging.error('[match_candidate] Return Not Okay Status : {}'
                          .format(response_dict.get('DxResponse').get('Status')
                                  )
                          )

    @staticmethod
    def _get_candidate_id_from_response(response_dict, action_type):
        # API Response format docs :
        # https://es-demo.daxtra.com/webservices/docs/add_candidate.html
        # https://es-demo.daxtra.com/webservices/docs/update_candidate.html

        status_code = response_dict.get('DxResponse').get('Status').get('Code')
        candidate_id = response_dict.get('DxResponse').get('Candidate').get(
            'CandidateId')
        if status_code and status_code == OK_STATUS:
            if candidate_id:
                return candidate_id
            else:
                logging.error('[{}] No Candidate ID in Daxtra Response'.format(
                    action_type))
        else:
            logging.error('[{}] Return Not Okay Status : {}'.format(
                action_type,
                response_dict.get('DxResponse').get('Status')))

    def set_scores_to_null_for_daxtra_vacancy_id(self, daxtra_vacancy_id):
        daxtra_candidates = DaxtraCandidate.query.filter(
            DaxtraCandidate.daxtra_vacancy_id == daxtra_vacancy_id,
            DaxtraCandidate.name.isnot(None)).all()

        for candidate in daxtra_candidates:
            candidate.score = None
            self.save(candidate, commit=False)
        db.session.commit()
