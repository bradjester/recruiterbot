# -*- coding: utf-8 -*-
"""
    app.helpers
    ~~~~~~~~~~~~~~~~

    helpers module
"""
import re
from datetime import datetime, date
from decimal import Decimal
from functools import wraps

import six
import sqlalchemy
from dateutil.tz import tzutc
from flask_login import login_required


def utc_now():
    return datetime.now(tz=tzutc())


def utc_date_today():
    return datetime.now(tz=tzutc()).date()


def format_date(dt):
    return dt.strftime('%Y-%m-%d')


def format_datetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def route(bp, *bpargs, **bpkwargs):
    """A decorator for routing. All routes should require login.
    :param bp: The Blueprint for the application.
    :param bpargs: Blueprint args.
    :param bpkwargs: Blueprint kwargs.
    """
    def decorator(f):
        @bp.route(*bpargs, **bpkwargs)
        @login_required
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f

    return decorator


class UTCDateTime(sqlalchemy.types.TypeDecorator):

    impl = sqlalchemy.types.DateTime

    def process_bind_param(self, value, engine):
        if value is not None:
            return value.astimezone(tzutc())

    def process_result_value(self, value, engine):
        if value is not None:
            return datetime(value.year, value.month, value.day,
                            value.hour, value.minute, value.second,
                            value.microsecond, tzinfo=tzutc())


def json_date_encoder(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else None


def serialize_for_json(value):
    if isinstance(value, list):
        return [serialize_for_json(v) for v in value]
    if isinstance(value, dict):
        for k, v in value.iteritems():
            value[k] = serialize_for_json(v)
        return value
    if isinstance(value, datetime) or isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    return value


def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def pagination_to_limit_offset(page=None, size=None):
    page = int(page) if page and isinstance(page, six.string_types) else page
    size = int(size) if size and isinstance(size, six.string_types) else size
    return size, page * size if page is not None and size else None
