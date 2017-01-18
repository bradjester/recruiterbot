# -*- coding: utf-8 -*-
"""
    app.base
    ~~~~~~~~~~~~~

    base module that all models should inherit
"""
import os

from sqlalchemy import func

from app.extensions import db
from app.helpers import UTCDateTime, serialize_for_json


def serialize_models(models):
    return [m.serialized_dict() for m in models]


class Base(db.Model):
    """
    Convenience base DB model class.
    """

    __abstract__ = True

    # All models should have id, created_at, and updated_at columns.
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)

    # Timestamp for when this instance was created (via the app), in UTC
    created_at = db.Column(
        UTCDateTime(timezone=True), default=func.current_timestamp(),
        server_default=func.current_timestamp(), nullable=False)

    # Timestamp for when this instance was last updated (via the app), in UTC
    updated_at = db.Column(UTCDateTime(timezone=True),
                           default=func.current_timestamp(),
                           server_default=func.current_timestamp(),
                           onupdate=func.current_timestamp(), nullable=False)

    # Used to serialize self in to a dictionary for JSON
    def serialized_dict(self):
        serialized = dict()
        for k in self.__dict__:
            value = self.__dict__[k]
            if '_sa_' != k[:4] and not issubclass(type(value), Base):
                serialized[k] = serialize_for_json(value)
        if getattr(self, 'display_name', None):
            serialized['display_name'] = self.display_name
        return serialized


class BaseDocument(Base):
    """
    Convenience base for document model classes.
    """
    __abstract__ = True

    key = db.Column(db.String(1024), nullable=False)
    doc_type = db.Column(db.String(50), nullable=False)

    @property
    def filename(self):
        return os.path.basename(self.key)
