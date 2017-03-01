# -*- coding: utf-8 -*-
from app.extensions import db
from app.modules.base import Base


class DaxtraVacancy(Base):
    __tablename__ = 'daxtra_vacancies'

    job_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'jobs.id',
            name='daxtra_vacancy_job_fk',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False)

    job = db.relationship(
        "Job",
        foreign_keys=job_id,
        backref=db.backref(
            'daxtra_vacancies',
            lazy='dynamic',
            cascade="all, delete-orphan"
        )
    )

    daxtra_id = db.Column(db.String(255), nullable=False)


class DaxtraCandidate(Base):
    __tablename__ = 'daxtra_candidates'

    daxtra_vacancy_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'daxtra_vacancies.id',
            name='daxtra_candidate_daxtra_vacancy_fk',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False)

    daxtra_vacancy = db.relationship(
        "DaxtraVacancy",
        foreign_keys=daxtra_vacancy_id,
        backref=db.backref(
            'daxtra_candidates',
            lazy='dynamic',
            cascade="all, delete-orphan"
        )
    )

    candidate_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'candidates.id',
            name='daxtra_candidate_candidate_fk',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False)

    candidate = db.relationship(
        "Candidate",
        foreign_keys=candidate_id,
        backref=db.backref(
            'daxtra_candidates',
            lazy='dynamic',
            cascade="all, delete-orphan"
        )
    )

    daxtra_id = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Float())
