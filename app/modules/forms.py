# -*- coding: utf-8 -*-
"""
    app.forms
    ~~~~~~~~~~~~~

    validators shared by all modules
"""
from wtforms.validators import StopValidation, Email, Length, ValidationError
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


class Unique(object):
    def __init__(self, model=None, pk_col_name="id", pk_field_name=None,
                 col_name=None, get_session=None, message=None,
                 ignore_if=None):
        self.model = model
        self.message = message
        self.col_name = col_name
        self.get_session = get_session
        self.pk_col_name = pk_col_name
        self.pk_field_name = pk_field_name
        self.ignore_if = ignore_if
        if not self.ignore_if:
            self.ignore_if = lambda field: not field.data

    @property
    def query(self):
        self._check_for_session(self.model)
        if self.get_session:
            return self.get_session().query(self.model)
        elif hasattr(self.model, 'query'):
            return getattr(self.model, 'query')
        else:
            raise Exception(
                'Validator requires either get_session or Flask-SQLAlchemy'
                ' styled query parameter'
            )

    def _check_for_session(self, model):
        if not hasattr(model, 'query') and not self.get_session:
            raise Exception('Could not obtain SQLAlchemy session.')

    def __call__(self, form, field):
        if self.ignore_if(field):
            return True

        # The primary key of the model.
        pk_col = getattr(self.model, self.pk_col_name)

        # The column that should be unique.
        unique_col = getattr(
            self.model, self.col_name if self.col_name else field.id
        )

        # The contents of the primary key's form field.
        pk = form[
            self.pk_field_name if self.pk_field_name else self.pk_col_name
        ].data

        # Query for a match on the unique column.
        query = self.model.query.filter(unique_col == form[field.id].data)
        if pk:
            # If the primary key was specified, exclude it since we obviously
            # want to allow updates on the model.
            query = query.filter(pk_col != pk)

        # If something already exists with this unique data, notify!
        if query.count() > 0:
            if self.message is None:
                self.message = field.gettext(u'Already exists.')
            raise ValidationError(self.message)
