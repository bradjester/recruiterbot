# -*- coding: utf-8 -*-
"""
    app.core
    ~~~~~~~~~~~~~

    core module
"""
import sqlalchemy as sa

from app.extensions import db


class AppError(Exception):
    """Base application error class."""


class AppFormError(Exception):
    """Raise when an error processing a form occurs."""

    def __init__(self, errors=None):
        self.errors = errors


class AppNotFoundError(AppError):
    """Base application not found error class."""


class AppConflictError(AppError):
    """Base application conflict error class."""


class AppUnexpectedState(AppError):
    """Base application unexpected state error class."""


class AppInvalidAttributeError(AppError):
    """When a specified attribute for an object is invalid."""


class Service(object):
    """A :class:`Service` instance encapsulates common SQLAlchemy model
    operations in the context of a :class:`Flask` application.
    """
    __abstract__ = True
    __model__ = None

    def _isinstance(self, model, raise_error=True):
        """Checks if the specified model instance matches the service's model.
        By default this method will raise a `ValueError` if the model is not
        the expected type.

        :param model: the model instance to check
        :param raise_error: flag to raise an error on a mismatch
        """
        rv = isinstance(model, self.__model__)
        if not rv and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.__model__))
        return rv

    @staticmethod
    def _preprocess_params(kwargs):
        """Returns a preprocessed dictionary of parameters. Used by default
        before creating a new instance or updating an existing instance.

        :param kwargs: a dictionary of parameters
        """
        kwargs.pop('csrf_token', None)
        return kwargs

    def columns_have_changes(self, model, *columns):
        attributes = self._get_model_attributes(model)
        has_changes = False
        for c in columns:
            if getattr(attributes, c.key).history.has_changes():
                has_changes = True
                break
        return has_changes

    def get_column_first_deleted_value(self, model, column):
        values = self.get_column_deleted_values(model, column)
        return values[0] if values else None

    def get_column_deleted_values(self, model, column):
        attributes = self._get_model_attributes(model)
        return getattr(attributes, column.key).history[2]

    def _get_model_attributes(self, model):
        self._isinstance(model)
        return sa.inspect(model).attrs

    def save_all(self, models, commit=True):
        try:
            saved_models = [self.save(m, commit=False, is_batch=True)
                            for m in models]
        except:
            db.session.rollback()
            raise
        if commit:
            db.session.commit()
        return saved_models

    def save(self, model, commit=True, is_batch=False):
        """Commits the model to the database and returns the model

        :param model: the model to save
        :param commit: commit the changes to the session, default is True
        :param is_batch: is this a batch save operation?
        """
        self._isinstance(model)
        model_inspection = sa.inspect(model)
        if model_inspection.transient:
            db.session.add(model)
        if commit:
            db.session.commit()
        return model

    def all(self, limit=None, offset=None):
        """
        Returns a generator containing all instances of the service's model.
        :param limit: an optional limit on the number of items returned.
        :param offset: an optional offset position.
        """
        return self.__model__.query.limit(limit).offset(offset).all()

    def get(self, _id):
        """Returns an instance of the service's model with the specified id.
        Returns `None` if an instance with the specified id does not exist.

        :param _id: the instance id
        """
        return self.__model__.query.get(_id)

    def get_all(self, *ids):
        """Returns a list of instances of the service's model with the specified
        ids.

        :param *ids: instance ids
        """
        return self.__model__.query.filter(self.__model__.id.in_(ids)).all()

    def find(self, limit=None, offset=None, **kwargs):
        """Returns a list of instances of the service's model filtered by the
        specified key word arguments.
        :param limit: an optional limit on the number of items returned.
        :param offset: an optional offset position.
        :param kwargs: filter parameters
        """
        return self.__model__.query.filter_by(**kwargs).limit(limit).offset(
            offset)

    def find_all(self, limit=None, offset=None, **kwargs):
        """Returns the all instances found of the service's model filtered by
        the specified key word arguments.
        :param limit: an optional limit on the number of items returned.
        :param offset: an optional offset position.
        :param kwargs: filter parameters
        """
        return self.find(limit=limit, offset=offset, **kwargs).all()

    def count(self, **kwargs):
        """Returns the count of instances found of the service's model
        filtered by the specified key word arguments.

        :param kwargs: filter parameters
        """
        return self.find(**kwargs).count()

    def first(self, **kwargs):
        """Returns the first instance found of the service's model filtered by
        the specified key word arguments.

        :param kwargs: filter parameters
        """
        return self.find(**kwargs).first()

    def get_or_404(self, id):
        """Returns an instance of the service's model with the specified id or
        raises an 404 error if an instance with the specified id does not
        exist.

        :param id: the instance id
        """
        return self.__model__.query.get_or_404(id)

    def new(self, **kwargs):
        """Returns a new, unsaved instance of the service's model class.

        :param kwargs: instance parameters
        """
        # pylint: disable=E1102
        return self.__model__(**self._preprocess_params(kwargs))

    def create(self, commit=True, **kwargs):
        """Returns a new, saved instance of the service's model class.

        :param commit: commit the changes to the session, default is True
        :param kwargs: instance parameters
        """
        return self.save(self.new(**kwargs), commit=commit)

    def update(self, model, commit=True, **kwargs):
        """Returns an updated instance of the service's model class.

        :param model: the model to update
        :param commit: commit the changes to the session, default is True
        :param kwargs: update parameters
        """
        self._isinstance(model)
        for k, v in self._preprocess_params(kwargs).items():
            setattr(model, k, v)
        self.save(model, commit=commit)
        return model

    def delete_all(self, models, commit=True):
        try:
            for model in models:
                self.delete(model, commit=False)
        except:
            db.session.rollback()
            raise
        if commit:
            db.session.commit()

    def delete(self, model, commit=True):
        """Immediately deletes the specified model instance.

        :param model: the model instance to delete
        :param commit: commit the changes to the session, default is True
        """
        self._isinstance(model)
        db.session.delete(model)
        if commit:
            db.session.commit()

    def autocomplete(self, attr_name, query, limit=10, include_id=False,
                     whole_obj=False):
        attr = getattr(self.__model__, attr_name, None)
        if not attr:
            raise AppInvalidAttributeError(
                '{} is not an attribute of {}'.format(
                    attr_name, self.__model__))

        if whole_obj:
            q = db.session.query(self.__model__)
        else:
            entities = [attr]
            if include_id:
                entities.append(getattr(self.__model__, "id"))
            q = db.session.query(*entities)

        q = q.filter(attr.ilike(query + "%")).\
            distinct().\
            order_by(attr_name).\
            limit(limit)

        if whole_obj:
            res = q.all()
        elif include_id:
            res = [{k: getattr(v, k) for k in ("id", attr_name)} for v in q]
        else:
            res = [getattr(v, attr_name) for v in q]
        return res

    def most_recently_created(self, **kwargs):
        return self.find_ordered_by_created_at_desc(**kwargs).first()

    def most_recently_updated(self, **kwargs):
        return self.find_ordered_by_updated_at_desc(**kwargs).first()

    def all_ordered_by_created_at_desc(self, limit=None, offset=None,
                                       **kwargs):
        return self.find_ordered_by_created_at_desc(
            limit=limit, offset=offset, **kwargs).all()

    def all_ordered_by_updated_at_desc(self, limit=None, offset=None,
                                       **kwargs):
        return self.find_ordered_by_updated_at_desc(
            limit=limit, offset=offset, **kwargs).all()

    def find_ordered_by_created_at_desc(self, limit=None, offset=None,
                                        **kwargs):
        return self.find_ordered_by(self.__model__.created_at.desc(),
                                    limit=limit, offset=offset, **kwargs)

    def find_ordered_by_updated_at_desc(self, limit=None, offset=None,
                                        **kwargs):
        return self.find_ordered_by(self.__model__.updated_at.desc(),
                                    limit=limit, offset=offset, **kwargs)

    def find_ordered_by(self, order_by, limit=None, offset=None, **kwargs):
        return self.__model__.query.filter_by(**kwargs)\
            .order_by(order_by).limit(limit).offset(offset)
