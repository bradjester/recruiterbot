#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~

    Manager module
"""
# pylint: disable=print-statement
import urllib.parse
from subprocess import call

import click
import flask
import pip
import sqlalchemy_utils
from flask_migrate import MigrateCommand, upgrade as upgrade_db
from flask_script import Manager, Shell

from app.extensions import db
from app.factory import create_app
from app.services import jobs_service, daxtra_vacancies_service, \
    candidates_service, daxtra_candidates_service
from fixtures import fixtures


def _make_context():
    return dict(app=flask.current_app, db=db)

manager = Manager(create_app)
manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=_make_context))


@manager.command
def resetdb():
    """Reset the database by dropping the db, creating it, and upgrading."""
    dropdb()
    createdb()
    upgrade_db()


@manager.command
def dropdb():
    """Drop the database"""
    app = flask.current_app
    if _dbexists(app):
        sqlalchemy_utils.drop_database(app.config['SQLALCHEMY_DATABASE_URI'])


@manager.command
def createdb():
    """Create the database."""
    app = flask.current_app
    if not _dbexists(app):
        sqlalchemy_utils.create_database(app.config['SQLALCHEMY_DATABASE_URI'])


@manager.command
def emptydb():
    """Empty the datbase of all contents."""
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()


def _dbexists(app):
    """Does the database exist?"""
    return sqlalchemy_utils.database_exists(
        app.config['SQLALCHEMY_DATABASE_URI'])


@manager.command
def routes():
    """Show all of the available routes."""
    output = []
    for rule in flask.current_app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        for key in options:
            if key[-2:] == 'id':
                options[key] = 1
        url = flask.url_for(rule.endpoint, **options)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(
            rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)


@manager.command
def upgrade_all_packages():
    """Upgrade all of the packages using pip."""
    for dist in pip.get_installed_distributions():
        call("pip install --upgrade " + dist.project_name, shell=True)


@manager.command
def load_fixtures():
    if click.confirm('Loading the fixtures will destroy all the data in your '
                     'database, are you sure you want to continue?',
                     default=True):
        emptydb()
        fixtures.load_fixtures()


@manager.command
def init_daxtra():
    print('Initializing Daxtra for Jobs')
    jobs = jobs_service.all()
    for job in jobs:
        job_id = job.id
        if not job.daxtra_vacancy:
            try:
                daxtra_vacancies_service.create_from_job(job)
            except Exception as e:
                db.session.rollback()
                print("Failed to create job for id {}: {}".format(
                    job_id,
                    str(e)
                ))

    print('Initializing Daxtra for Candidates')
    candidates = candidates_service.all()
    for candidate in candidates:
        candidate_id = candidate.id
        if (candidate.resume_key and candidate.bot.job.daxtra_vacancy and
                not candidate.daxtra_candidate):
            try:
                daxtra_candidates_service.create_from_candidate(candidate)
            except Exception as e:
                db.session.rollback()
                print("Failed to create candidate for id {}: {}".format(
                    candidate_id,
                    str(e)
                ))

    print('Finished initializing Daxtra')


manager.add_option('-c', '--config', dest='config', required=False)

if __name__ == "__main__":
    manager.run()
