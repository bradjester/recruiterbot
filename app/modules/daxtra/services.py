# -*- coding: utf-8 -*-

import logging
from abc import ABCMeta
from xml.etree.ElementTree import SubElement

from app.core import Service
from app.extensions import db
from app.modules.daxtra.models import DaxtraVacancy, DaxtraCandidate

from .helpers import get_base_daxtra_request_xml, base_64_encode_document,\
    send_req_and_get_response_dict, prettify_xml, dict_to_xml
from .constants import ADD_CANDIDATE_ACTION, ADD_VACANCY_ACTION, \
    UPDATE_CANDIDATE_ACTION, UPDATE_VACANCY_ACTION, \
    MATCH_CANDIDATE_ACTION, OK_STATUS
from .errors import DaxtraResponseIdNotFound, DaxtraResponseResultNotFound, \
    DaxtraResponseStatusNotOkay


class BaseDaxtraService(metaclass=ABCMeta, Service):

    def _send_get_response_id_from_daxtra(self, dx_request,
                                          vacancy_or_candidate_elem, file_url,
                                          action):

        if action == UPDATE_CANDIDATE_ACTION or action == ADD_CANDIDATE_ACTION:
            profile_elem = SubElement(vacancy_or_candidate_elem, 'Profile')
            profile_elem.text = base_64_encode_document(file_url)

            response_dict = send_req_and_get_response_dict(dx_request)
            try:
                vacancy_id = self._get_id_from_response_dict(response_dict,
                                                             action)
                return vacancy_id
            except (DaxtraResponseIdNotFound,
                    DaxtraResponseStatusNotOkay):
                logging.exception(self._get_pretty_action_req_resp_str(
                    action, dx_request, response_dict)
                )

    @staticmethod
    def _get_pretty_action_req_resp_str(action, req, resp_dict):
        return '\n'.join(['Action : ',
                          action,
                          'Daxtra Request:',
                          # only first 400 chars because req is large
                          prettify_xml(req)[0:min(len(req)-1, 400)],
                          'Daxtra Response: ',
                          prettify_xml(dict_to_xml(resp_dict))]
                         )

    @staticmethod
    def _get_id_from_response_dict(response_dict, action):
        # API Response format docs :
        # https://es-demo.daxtra.com/webservices/docs/add_vacancy.html
        # https://es-demo.daxtra.com/webservices/docs/update_vacancy.html
        # https://es-demo.daxtra.com/webservices/docs/add_candidate.html
        # https://es-demo.daxtra.com/webservices/docs/update_candidate.html

        vacancy_or_candidate = 'Vacancy' \
            if (action == UPDATE_VACANCY_ACTION or
                action == ADD_VACANCY_ACTION) else 'Candidate'

        vacancy_or_candidate_id = vacancy_or_candidate + 'Id'

        status_code = response_dict.get('DxResponse').get('Status').get('Code')
        returned_id = response_dict.get('DxResponse').get(
            vacancy_or_candidate).get(vacancy_or_candidate_id)

        if status_code and status_code == OK_STATUS:
            if not returned_id:
                raise DaxtraResponseIdNotFound
            return returned_id
        else:
            raise DaxtraResponseStatusNotOkay


class DaxtraVacanciesService(BaseDaxtraService):
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
        ret_daxtra_id = self._update_daxtra_vacancy_and_get_id(
            daxtra_vacancy.daxtra_id, url)

        # Set the daxtra scores for this job.id to null
        if daxtra_vacancy.daxtra_id == ret_daxtra_id:  # all went well
            self.daxtra_candidates_service.set_scores_to_null_for_daxtra_vacancy_id(  # noqa
                daxtra_vacancy.daxtra_id
            )

    def _create_daxtra_vacancy_and_get_id(self, file_url):
        action = ADD_VACANCY_ACTION
        dx_request = get_base_daxtra_request_xml(action)

        vacancy_elem = SubElement(dx_request, 'Vacancy')

        return self._send_get_response_id_from_daxtra(dx_request, vacancy_elem,
                                                      file_url, action)

    def _update_daxtra_vacancy_and_get_id(self, daxtra_id, file_url):
        action = UPDATE_VACANCY_ACTION
        dx_request = get_base_daxtra_request_xml(action)

        vacancy_elem = SubElement(dx_request, 'Vacancy')

        vacancy_id_elem = SubElement(vacancy_elem, 'VacancyId')
        vacancy_id_elem.text = daxtra_id

        return self._send_get_response_id_from_daxtra(dx_request, vacancy_elem,
                                                      file_url, action)


class DaxtraCandidatesService(BaseDaxtraService):
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
        action = ADD_CANDIDATE_ACTION
        dx_request = get_base_daxtra_request_xml(action)

        candidate_elem = SubElement(dx_request, 'Candidate')

        return self._send_get_response_id_from_daxtra(dx_request,
                                                      candidate_elem,
                                                      file_url,
                                                      action)

    def update_from_candidate(self, candidate):
        url = self.static_storage_service.generate_signed_url(
            candidate.resume_key)

        daxtra_candidate = self.find(candidate_id=candidate.id)

        ret_daxtra_id = self._update_daxtra_candidate_and_get_id(
            daxtra_candidate.daxtra_id, url)

        # Set the daxtra scores for this candidate.id to null
        if daxtra_candidate.daxtra_id == ret_daxtra_id:  # all went well
            daxtra_candidate.score = None
            self.save(daxtra_candidate)
        else:
            logging.error('Error while updating candidate with id {} on daxtra'
                          ' db. Id returned from daxtra is not the same.')

    def _update_daxtra_candidate_and_get_id(self, daxtra_id, file_url):
        action = UPDATE_CANDIDATE_ACTION
        dx_request = get_base_daxtra_request_xml(action)

        vacancy_elem = SubElement(dx_request, 'Vacancy')

        vacancy_id_elem = SubElement(vacancy_elem, 'VacancyId')
        vacancy_id_elem.text = daxtra_id

        return self._send_get_response_id_from_daxtra(dx_request, vacancy_elem,
                                                      file_url, action)

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
        daxtra_candidate.score = self._fetch_daxtra_score_for_candidate(
            daxtra_candidate)
        return self.save(daxtra_candidate, commit=commit)

    def _fetch_daxtra_score_for_candidate(self, daxtra_candidate):
        dx_request = get_base_daxtra_request_xml(
            MATCH_CANDIDATE_ACTION,
            options='details'
        )
        daxtra_vacancy = daxtra_candidate.daxtra_vacancy

        candidate_elem = SubElement(dx_request, 'Candidate')

        dx_candidate_id_elem = SubElement(candidate_elem, 'CandidateId')
        dx_candidate_id_elem.text = daxtra_candidate.daxtra_id

        vacancy_elem = SubElement(dx_request, 'Vacancy')
        structured_options = SubElement(vacancy_elem, 'StructuredOptions')

        dx_vacancy_id_elem = SubElement(structured_options, 'VacancyId')
        dx_vacancy_id_elem.text = daxtra_vacancy

        response_dict = send_req_and_get_response_dict(dx_request)

        try:
            return self._get_score_from_response(response_dict)
        except (DaxtraResponseResultNotFound, DaxtraResponseStatusNotOkay):
            logging.exception(self._get_pretty_action_req_resp_str(
                MATCH_CANDIDATE_ACTION, dx_request, response_dict
            ))

        except ValueError:
            logging.exception('Score obtained is not of type float')

    @staticmethod
    def _get_score_from_response(response_dict):
        # API Response format docs :
        # https://es-demo.daxtra.com/webservices/docs/match_candidate.html

        status_code = response_dict.get('DxResponse').get('Status').get('Code')
        result = response_dict.get('DxResponse').get('Results').get('Result')

        if status_code and status_code == OK_STATUS:
            if not result:
                raise DaxtraResponseResultNotFound
            score = float(result.get('DxResponse').get(
                'Results').get('Result').get('Score'))
            return score
        else:
            raise DaxtraResponseStatusNotOkay

    def set_scores_to_null_for_daxtra_vacancy_id(self, daxtra_vacancy_id):
        daxtra_candidates = DaxtraCandidate.query.filter(
            DaxtraCandidate.daxtra_vacancy_id == daxtra_vacancy_id,
            DaxtraCandidate.name.isnot(None)).all()

        for candidate in daxtra_candidates:
            candidate.score = None
            self.save(candidate, commit=False)
        db.session.commit()
