# -*- coding: utf-8 -*-
import json
import os
from uuid import uuid4

from flask_security.utils import encrypt_password

from app.extensions import db
from app.helpers import utc_now
from app.services import users_service, companies_service, roles_service, \
    jobs_service, bots_service, candidates_service, webhook_service

MESSAGES_FILE = os.path.join(os.path.dirname(__file__), 'data/messages.json')

BOTS_DATA = [
    dict(
        bot_url="http://facebook.com/{}/{}-passive-bot",
        channel_type="fb",
        chat_type="passive",
    ),
    dict(
        bot_url="http://facebook.com/{}/{}-active-bot",
        channel_type="fb",
        chat_type="active",
    ),
    dict(
        bot_url="http://{}.com/{}/passive-bot",
        channel_type="web",
        chat_type="passive",
    ),
    dict(
        bot_url="http://{}.com/{}/active-bot",
        channel_type="web",
        chat_type="active",
    ),
]


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


def _load_messages():
    with open(MESSAGES_FILE) as data_file:
        return json.load(data_file)["messages"]


def _create_job(company, title, hiring_company, is_published=True,
                candidates_per_job=0, messages=None):
    job = jobs_service.create(
        company=company,
        title=title,
        hiring_company=hiring_company,
        location="Hong Kong",
        work_type="Full-time",
        expected_salary="50000",
        is_published=is_published,
        uuid=uuid4(),
        jd_file_key="job_description/59d870a7-0493-48be-8c51-c94ac8e2bb5f/"
                    "chicken.pdf",
        commit=False,
    )

    for bot_data in BOTS_DATA:
        bot = _create_bot(job, company, bot_data)
        for _ in range(candidates_per_job):
            _create_candidate(bot, company, messages=messages)

    return job


@static_vars(counter=1)
def _create_bot(job, company, bot_data):
    _create_bot.counter += 1
    chat_type = bot_data['chat_type']
    channel_type = bot_data['channel_type']
    if (company.name == "Droste" and chat_type == "passive" and
            channel_type == "web" and job.is_published):
        bot_id = 28083
        bot_url = "https://api.motion.ai/webchat/28083?sendBtn=SEND" \
                  "&inputBox=Type+something..." \
                  "&token=fad2f73d4b05b27622c18de72f5c5a34"
    elif (company.name == "Droste" and chat_type == "active" and
            channel_type == "fb" and job.is_published):
        bot_id = 27833
        bot_url = "https://www.facebook.com" \
                  "/AI-Chatbot-Test-Page-704073659770212/"
    else:
        bot_id = _create_bot.counter
        bot_url = bot_data['bot_url'].format(company.name, job.id)

    return bots_service.create(
        job=job,
        company=company,
        bot_id=bot_id,
        bot_url=bot_url,
        channel_type=channel_type,
        chat_type=chat_type,
        commit=False,
    )


@static_vars(counter=0)
def _create_candidate(bot, company, status="New", rating=None, messages=None):
    _create_candidate.counter += 1
    candidate = candidates_service.create(
        bot=bot,
        company=company,
        name="Candidate {}".format(_create_candidate.counter),
        resume_key="job_description/59d870a7-0493-48be-8c51-c94ac8e2bb5f/"
                   "chicken.pdf",
        session_id="{}".format(_create_candidate.counter),
        status=status,
        rating=rating,
        commit=False,
    )

    for message in messages:
        webhook_service.create_message_from_data(
            bot,
            candidate,
            company,
            message,
            commit=False,
        )


def load_fixtures():
    messages = _load_messages()
    admin_role = roles_service.create(name="admin", commit=False)
    user_role = roles_service.create(name="user", commit=False)

    users_service.create(
        email="admin@jobrobin.com",
        password=encrypt_password("password"),
        active=True,
        confirmed_at=utc_now(),
        first_name="Admin",
        surname="JobRobin",
        roles=[admin_role],
        commit=False,
    )

    # Acme Stuff
    acme_company = companies_service.create(name="Acme")

    users_service.create(
        email="user1@acme.hk",
        password=encrypt_password("password"),
        active=True,
        confirmed_at=utc_now(),
        first_name="User1",
        surname="Acme",
        company=acme_company,
        roles=[user_role],
        commit=False,
    )

    users_service.create(
        email="user2@acme.hk",
        password=encrypt_password("password"),
        active=True,
        confirmed_at=utc_now(),
        first_name="User2",
        surname="Acme",
        company=acme_company,
        roles=[user_role],
        commit=False,
    )

    _create_job(
        acme_company,
        "Published Job",
        "IBM",
        candidates_per_job=2,
        messages=messages,
    )

    _create_job(
        acme_company,
        "Unpublished Job",
        "Google",
        is_published=False
    )

    # Droste Stuff
    droste_company = companies_service.create(name="Droste", commit=False)

    users_service.create(
        email="user1@droste.hk",
        password=encrypt_password("password"),
        active=True,
        confirmed_at=utc_now(),
        first_name="User1",
        surname="Droste",
        company=droste_company,
        roles=[user_role],
        commit=False,
    )

    users_service.create(
        email="user2@droste.hk",
        password=encrypt_password("password"),
        active=True,
        confirmed_at=utc_now(),
        first_name="User2",
        surname="Droste",
        company=droste_company,
        roles=[user_role],
        commit=False,
    )

    _create_job(
        droste_company,
        "Data Engineer",
        "Droste",
        candidates_per_job=4,
        messages=messages,
    )

    _create_job(
        droste_company,
        "Programmer",
        "Droste",
        is_published=False
    )

    db.session.commit()
