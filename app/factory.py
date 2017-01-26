# -*- coding: utf-8 -*-
"""
    app.factory
    ~~~~~~~~~~~~~~~~

    factory module
"""
import logging
import sys

from flask import Flask, render_template
from flask_babel import Babel
from flask_login import current_user
from flask_security import logout_user

from app import assets
from app.extensions import db, migrate
from app.middleware import HTTPMethodOverrideMiddleware
from app.modules.admin import init_admin
from app.modules.api.views import api_bp
from app.modules.frontend.views import frontend_bp
from app.modules.motionai.views import webhook_bp
from app.modules.jobs.views import candidates_bp
from app.modules.jobs.views import job_bp
from app.modules.users import init_security
from app.services import users_service, static_storage_service, aws_ses_service

BLUEPRINTS = [
    api_bp,
    frontend_bp,
    webhook_bp,
    candidates_bp,
    job_bp,
]

BLUEPRINTS_NO_CSRF = [
    webhook_bp
]

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format=LOG_FORMAT)


def create_app(config=None):
    """Returns a :class:`Flask` application instance configured with common
    functionality for the app.

    :param config: an optional config file to override other settings.
    """
    app = Flask(__name__, instance_relative_config=True)

    load_configuration(app, config=config)
    configure_middleware(app)
    configure_before_request_security(app)
    Babel(app)
    init_db(app)
    assets.init_app(app)
    init_security(app, users_service, BLUEPRINTS_NO_CSRF)
    init_security_send_mail(app)
    configure_error_handlers(app)
    configure_blueprints(app)
    init_admin(app)
    init_view_helpers(app)

    return app


def load_configuration(app, config=None):
    app.config.from_object('app.settings')
    app.config.from_pyfile('settings.cfg', silent=True)
    app.config.from_object(config)


def configure_middleware(app):
    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)


def configure_before_request_security(app):
    """Ensure user is active"""
    @app.before_request
    def ensure_user_active():
        if current_user and not current_user.is_active:
            logout_user()


def init_db(app):
    if app.config['DATABASE_PASSWORD']:
        user_pass = '{}:{}'.format(app.config['DATABASE_USERNAME'],
                                   app.config['DATABASE_PASSWORD'])
    else:
        user_pass = app.config['DATABASE_USERNAME']

    uri = '{}://{}@{}:{}/{}'.format(
        app.config['DATABASE_CONNECTOR'],
        user_pass,
        app.config['DATABASE_HOST'],
        app.config['DATABASE_PORT'],
        app.config['DATABASE_NAME'])
    app.config['SQLALCHEMY_DATABASE_URI'] = uri

    db.init_app(app)
    migrate.init_app(app, db)


def init_security_send_mail(app):
    # Override Flask-Security mail sending to use AWS SES.
    app.extensions['security'].send_mail_task(aws_ses_service.send_message)


def configure_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(*_):
        return render_template("errors/forbidden.html"), 403

    @app.errorhandler(404)
    def page_not_found(*_):
        return render_template("errors/page_not_found.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        logger = logging.getLogger(__name__)
        logger.error(u'Server error: {}'.format(error))
        return render_template("errors/server_error.html"), 500


def configure_blueprints(app):
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)


def init_view_helpers(app):
    app.jinja_env.add_extension('jinja2.ext.do')

    @app.template_filter('shorten')
    def shorten_filter(s):
        if s and len(s) > 25:
            return s[:24] + u"…"
        return s

    @app.template_filter('no_none')
    def no_none_filter(s):

        if "None" in str(s):
            return str(s).replace("None", "")
        return s

    @app.context_processor
    def view_helpers():
        return dict(
            generate_signed_url=static_storage_service.generate_signed_url
        )
