# -*- coding: utf-8 -*-
"""
    app.modules.daxtra.helpers
    ~~~~~~~~~~~~~~~~~~~~~

    Daxtra module helpers
"""
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

from urllib.request import urlopen
import base64

from flask import current_app
import xmltodict
import requests

from .constants import DAXTRA_REQUEST_HEADERS


def base_64_encode_document(doc_url):
    cv_file_handle = urlopen(doc_url)
    txt = cv_file_handle.read()
    return base64.b64encode(txt).decode('utf-8')


def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')


def get_base_daxtra_request_xml(action_string, options=None):
    """ This function returns the base xml object that is used
    for all the requests made to Daxtra's Search and Match API
    This object is extected to be manipulated further for each specific request

    Format:

    <?xml version="1.0" encoding="utf-8"?>
    <DxRequest>
      <Action>match_vacancy</Action>
      <!-- optional <Options></Options> !-->
      <Username>string</Username>
      <Password>string</Password>
      <Database>string</Database>
      <!-- Request specific tags go here !-->

    </DxRequest>
    """
    dx_request = Element('DxRequest')

    action = SubElement(dx_request, 'Action')
    action.text = action_string

    if options:
        options_elem = SubElement(dx_request, 'Options')
        options_elem.text = options

    username = SubElement(dx_request, 'Username')
    username.text = current_app.config.get('DAXTRA_USERNAME')

    password = SubElement(dx_request, 'Password')
    password.text = current_app.config.get('DAXTRA_PASSWORD')

    database = SubElement(dx_request, 'Database')
    database.text = current_app.config.get('DAXTRA_DB_NAME')

    return dx_request


def xml_to_dict(xml_response_str):
    return xmltodict.parse(xml_response_str)


def dict_to_xml(_dict):
    return xmltodict.unparse(_dict)


def send_req_and_get_response_dict(dx_request_xml_obj):

    payload = tostring(dx_request_xml_obj, encoding='utf-8')

    response = requests.post(current_app.config.get('DAXTRA_API_URL'),
                             headers=DAXTRA_REQUEST_HEADERS,
                             data=payload)

    return xml_to_dict(response.content.decode('utf-8'))
