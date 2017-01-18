# -*- coding: utf-8 -*-
"""
    app.forms
    ~~~~~~~~~~~~~

    validators shared by all modules
"""
from wtforms.validators import StopValidation, Email, Length
from wtforms.fields import StringField


class NotNoneInputRequired(object):
    """
    Validates that numeric input was provided for this field.

    Note there is a distinction between this and InputRequired in that
    NotNoneInputRequired verifies that form-input data was provided and is not
    None, and InputRequired will consider 0 or False values as non-inputs.
    """
    field_flags = ('required', )

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if not field.raw_data or field.raw_data[0] is None:
            if self.message is None:
                message = field.gettext('This field is required.')
            else:
                message = self.message

            field.errors[:] = []
            raise StopValidation(message)


class OptionalEmail(Email):

    def __call__(self, form, field):  # NOQA
        if field.data and len(field.data) > 0:
            super(OptionalEmail, self).__call__(form, field)


class EmailField(StringField):
    validators = [Length(max=255), OptionalEmail()]


class NullStringField(StringField):
    """
    A StringField that coerces empty strings into NULL.
    """
    def __init__(self, **kwargs):
        super(NullStringField, self).__init__(**kwargs)
        self.filters += lambda x: x or None,


class StripStringField(StringField):
    def __init__(self, **kwargs):

        kwargs['filters'] = kwargs.get('filters', []) + [strip_whitespace]
        super(StripStringField, self).__init__(**kwargs)


class StripNullStringField(StringField):
    def __init__(self, **kwargs):

        kwargs['filters'] = kwargs.get('filters', []) + \
                            [strip_whitespace, lambda x: x or None]
        super(StripNullStringField, self).__init__(**kwargs)


def strip_whitespace(value):
    if value is not None and hasattr(value, 'strip'):
        return value.strip()
    return value
