# -*- coding: utf-8 -*-
"""
    app.settings
    ~~~~~~~~~~~~~~~

    settings module
"""
import os

if 'IS_DEV' not in os.environ:
    IS_DEV = True
else:
    IS_DEV = (os.environ['IS_DEV'].lower() == "true" or
              os.environ['IS_DEV'] == "1")

if 'DEBUG' not in os.environ:
    DEBUG = True
else:
    DEBUG = os.environ['DEBUG'].lower() == "true" or os.environ['DEBUG'] == "1"

# Flask Secret Key for sessions. We should override for other environments.
SECRET_KEY = os.getenv('SECRET_KEY', 'xKm0li7uR6jIyW7NHFQ9EWYhnDre')
FLASH_MESSAGES = True

SQLALCHEMY_TRACK_MODIFICATIONS = False

# These should be set together if you want to override.
DATABASE_CONNECTOR = 'mysql+mysqldb'
DATABASE_USERNAME = os.getenv('RDS_USERNAME', 'root')
DATABASE_PASSWORD = os.getenv('RDS_PASSWORD', 'root')
DATABASE_HOST = os.getenv('RDS_HOSTNAME', '127.0.0.1')
DATABASE_PORT = os.getenv('RDS_PORT', 3306)
DATABASE_NAME = os.getenv('RDS_DB_NAME', 'skynet')

# Flask-Security
SECURITY_PASSWORD_HASH = 'bcrypt'
SECURITY_PASSWORD_SALT = os.getenv(
    'SECURITY_PASSWORD_SALT', 'hCi3oiQUG0i9u4AGZScX7oqx2Pzy')
SECURITY_POST_LOGIN_VIEW = '/'
# Register users.
SECURITY_REGISTERABLE = True
# Track the user logins.
SECURITY_TRACKABLE = True
# Users can reset their passwords.
SECURITY_RECOVERABLE = True
# Users can change their passwords.
SECURITY_CHANGEABLE = True
# Security Email Sender.
SECURITY_EMAIL_SENDER = os.getenv('SECURITY_EMAIL_SENDER',
                                  'admin@precruiter.co')
# Welcome email subject.
SECURITY_EMAIL_SUBJECT_REGISTER = u'Welcome to JobRobin!'
# Reset / Set password subject.
SECURITY_EMAIL_SUBJECT_PASSWORD_NOTICE = u'Your JobRobin password ' \
                                         u'has been set!'
# Changed password subject.
SECURITY_EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE = u'Your JobRobin ' \
                                                u'password has been changed!'
# Reset password subject.
SECURITY_EMAIL_SUBJECT_PASSWORD_RESET = u'Instructions to reset your ' \
                                        u'JobRobin password!'


# Mail configuration
BOUNCES_AND_COMPLAINTS_EMAIL = os.getenv(
    'BOUNCES_AND_COMPLAINTS_EMAIL', 'admin@precruiter.co')

# Flask-Login
# https://flask-login.readthedocs.org/en/latest/#protecting-views
LOGIN_DISABLED = False

# AWS Configuration for DEV ONLY. Other values will be used for staging / prod.
AWS_ACCESS_KEY_ID = 'AKIAJAM3R7UAJOHLF37Q'
AWS_SECRET_ACCESS_KEY = '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'
AWS_REGION_NAME = 'us-east-1'

# AWS S3 Bucket for environment should be an env variable.
AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET', 'skynet-app-dev')
