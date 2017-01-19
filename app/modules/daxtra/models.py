# -*- coding: utf-8 -*-
"""
    app.modules.daxtra.models
    ~~~~~~~~~~~~~~~~~~~~~

    Daxtra module models
"""
from app.extensions import db
from app.modules.base import Base


class Daxtra(Base):
    __tablename__ = 'daxtra'

    candidate_id = db.Column(
        db.Integer,
        db.ForeignKey('candidates.id', name='daxtra_candidate_fk',
                      onupdate='CASCADE', ondelete='CASCADE'))

    candidate = db.relationship(
        "Candidate",
        single_parent=True,
        foreign_keys=candidate_id)

    job_id = db.Column(
        db.Integer,
        db.ForeignKey('jobs.id', name='daxtra_job_fk',
                      onupdate='CASCADE', ondelete='CASCADE'))

    job = db.relationship(
        "Job", foreign_keys=job_id)

    # Should be double if Daxtra provides us with a fractional score
    score = db.Column(db.Integer)

    def __str__(self):
        return self.candidate_id
