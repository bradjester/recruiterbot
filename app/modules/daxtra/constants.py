# -*- coding: utf-8 -*-
"""
    app.modules.daxtra.constants
    ~~~~~~~~~~~~~~~~~~~~~

    Daxtra constants
"""
from flask import current_app

DAXTRA_API_URL = 'http://es-demo.daxtra.com/ws/dispatch?username={}&password={}&database={}'.format(  # noqa
    current_app.get('DAXTRA_USERNAME'),
    current_app.get('DAXTRA_PASSWORD'),
    current_app.get('DAXTRA_DB_NAME')
)

DAXTRA_REQUEST_HEADERS = {'Content-Type': 'text/xml'}

# API Actions/Request Types
ADD_CANDIDATE_ACTION = 'add_candidate'
ADD_VACANCY_ACTION = 'add_vacancy'
UPDATE_CANDIDATE_ACTION = 'update_candidate'
UPDATE_VACANCY_ACTION = 'update_vacancy'
MATCH_CANDIDATE_ACTION = 'match_candidate'

# DAXTRA STATUS CODES (IMPORTANT ONES ONLY)
OK_STATUS = '100'
