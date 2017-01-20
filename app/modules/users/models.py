# -*- coding: utf-8 -*-
"""
    app.modules.users.models
    ~~~~~~~~~~~~~~~~~~~~~

    User models
"""
from flask_security import UserMixin, RoleMixin

from app.extensions import db
from app.helpers import UTCDateTime
from app.modules.base import Base
from .constants import ADMIN_ROLE_NAME

roles_users = db.Table(
    'roles_users',
    db.Column(
        'user_id', db.Integer(),
        db.ForeignKey(
            'users.id', name='roles_users_user_fk', ondelete="CASCADE")),
    db.Column(
        'role_id', db.Integer(),
        db.ForeignKey(
            'roles.id', name='roles_users_role_fk', ondelete="CASCADE")),
    db.PrimaryKeyConstraint('user_id', 'role_id'))


class Role(RoleMixin, Base):
    __tablename__ = 'roles'

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    @property
    def display_name(self):
        return self.name

    def __str__(self):
        return self.name


class User(UserMixin, Base):
    __tablename__ = 'users'

    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(UTCDateTime())
    first_name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    last_login_at = db.Column(UTCDateTime())
    current_login_at = db.Column(UTCDateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    company_id = db.Column(
        db.Integer,
        db.ForeignKey('companies.id', name='user_company_fk',
                      onupdate='CASCADE', ondelete='SET NULL'))

    company = db.relationship(
        "Company",
        foreign_keys=company_id)

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    @property
    def is_admin(self):
        return self.has_role(ADMIN_ROLE_NAME)


class Company(Base):
    __tablename__ = 'companies'

    name = db.Column(db.String(100), unique=True, nullable=False)
