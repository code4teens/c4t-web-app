from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    func,
    Integer,
    JSON,
    SmallInteger,
    String
)
from sqlalchemy.orm import relationship
from sqlalchemy.util.langhelpers import hybridmethod, hybridproperty

from config import tz
from database import Base


class User(UserMixin, Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    password = Column(String(60), nullable=False)
    name = Column(String(64), nullable=False)
    discriminator = Column(String(4), nullable=False)
    display_name = Column(String(64), nullable=False)
    cohort_id = Column(SmallInteger, ForeignKey('cohort.id'), nullable=True)
    xp = Column(Integer, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_updated = Column(DateTime, nullable=False, default=func.now())

    bots = relationship(
        'Bot', back_populates='user', order_by='Bot.created_at'
    )
    enrolments = relationship(
        'Enrolment', back_populates='user', order_by='Enrolment.id'
    )
    evals_evaluator = relationship(
        'Eval',
        foreign_keys='Eval.evaluator_id',
        back_populates='evaluator',
        order_by='Eval.id'
    )
    evals_evaluatee = relationship(
        'Eval',
        foreign_keys='Eval.evaluatee_id',
        back_populates='evaluatee',
        order_by='Eval.id'
    )

    @hybridmethod
    def evals(self, cohort_id):
        evals = self.evals_evaluator + self.evals_evaluatee
        evals.sort(key=lambda x: x.id)
        filtered_evals = list(
            filter(lambda x: x.cohort_id == cohort_id, evals)
        )

        return filtered_evals

    @hybridmethod
    def incomplete_evals(self, cohort_id):
        incomplete_evals = [
            eval for eval in self.evals(cohort_id)
            if eval.review is None or eval.feedback is None
        ]

        return incomplete_evals


class Bot(Base):
    __tablename__ = 'bot'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(64), nullable=False)
    discriminator = Column(String(4), nullable=False)
    display_name = Column(String(64), nullable=False)
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    msg_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_updated = Column(DateTime, nullable=False, default=func.now())

    user = relationship('User', back_populates='bots')


class Cohort(Base):
    __tablename__ = 'cohort'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(32), nullable=False)
    nickname = Column(String(16), nullable=False)
    duration = Column(SmallInteger, nullable=False)
    start_date = Column(DateTime, nullable=False)
    review_schema = Column(JSON, nullable=True)
    feedback_schema = Column(JSON, nullable=True)

    enrolments = relationship(
        'Enrolment', back_populates='cohort', order_by='Enrolment.id'
    )
    evals = relationship('Eval', back_populates='cohort', order_by='Eval.id')


class Enrolment(Base):
    __tablename__ = 'enrolment'
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    cohort_id = Column(SmallInteger, ForeignKey('cohort.id'), nullable=False)

    user = relationship('User', back_populates='enrolments')
    cohort = relationship('Cohort', back_populates='enrolments')


class Eval(Base):
    __tablename__ = 'eval'
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    evaluator_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    evaluatee_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    cohort_id = Column(SmallInteger, ForeignKey('cohort.id'), nullable=False)
    date = Column(Date, nullable=False)
    review = Column(JSON, nullable=True)
    feedback = Column(JSON, nullable=True)

    evaluator = relationship(
        'User', foreign_keys=[evaluator_id], back_populates='evals_evaluator')
    evaluatee = relationship(
        'User', foreign_keys=[evaluatee_id], back_populates='evals_evaluatee')
    cohort = relationship('Cohort', back_populates='evals')

    @hybridproperty
    def day(self):
        delta = self.date - self.cohort.start_date

        return delta.days + 1

    @hybridproperty
    def lapse(self):
        delta = datetime.now(tz).date() - self.date

        return delta.days

    @hybridproperty
    def is_complete(self):
        if self.review is None or self.feedback is None:
            return False

        return True
