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

import flask
import pip
import sqlalchemy_utils
from flask_migrate import MigrateCommand, upgrade as upgrade_db
from flask_script import Manager, Shell

from app.extensions import db
from app.factory import create_app


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

manager.add_option('-c', '--config', dest='config', required=False)

if __name__ == "__main__":
    manager.run()
