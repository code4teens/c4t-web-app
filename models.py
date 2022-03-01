from datetime import datetime, timedelta

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

from database import Base
from utils import tz


class User(UserMixin, Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    password = Column(String(60), nullable=False)
    name = Column(String(64), nullable=False)
    discriminator = Column(String(4), nullable=False)
    display_name = Column(String(64), nullable=False)
    xp = Column(Integer, nullable=False, default=0)
    is_admin = Column(Boolean, nullable=False, default=False)
    api_key = Column(String(43), nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_updated = Column(DateTime, nullable=False, default=func.now())

    bots = relationship(
        'Bot', back_populates='user', order_by='Bot.created_at'
    )
    channels = relationship(
        'Channel', back_populates='user', order_by='Channel.created_at'
    )
    enrolments = relationship(
        'Enrolment', back_populates='user', order_by='Enrolment.id'
    )
    evals_as_evaluator = relationship(
        'Eval',
        foreign_keys='Eval.evaluator_id',
        back_populates='evaluator',
        order_by='Eval.id'
    )
    evals_as_evaluatee = relationship(
        'Eval',
        foreign_keys='Eval.evaluatee_id',
        back_populates='evaluatee',
        order_by='Eval.id'
    )

    @hybridmethod
    def evals(self, cohort_id):
        evals = self.evals_as_evaluator + self.evals_as_evaluatee
        evals.sort(key=lambda x: x.id)
        filtered_evals = list(
            filter(lambda x: x.cohort_id == cohort_id, evals)
        )

        return filtered_evals

    @hybridmethod
    def daily_evals(self, cohort_id, start_date, day):
        date = start_date + timedelta(days=day)
        filtered_evals = list(
            filter(lambda x: x.date == date, self.evals(cohort_id))
        )

        return filtered_evals

    @hybridmethod
    def incomplete_evals(self, cohort_id):
        incomplete_evals = [
            eval for eval in self.evals(cohort_id)
            if eval.review is None or eval.feedback is None
        ]

        return incomplete_evals

    @hybridmethod
    def daily_incomplete_evals(self, cohort_id, start_date, day):
        incomplete_evals = [
            eval for eval in self.daily_evals(cohort_id, start_date, day)
            if eval.review is None or eval.feedback is None
        ]

        return incomplete_evals

    @hybridproperty
    def username(self):
        username = f'{self.name}#{self.discriminator}'

        return username


class Bot(Base):
    __tablename__ = 'bot'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(64), nullable=True)
    discriminator = Column(String(4), nullable=True)
    display_name = Column(String(64), nullable=True)
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    cohort_id = Column(SmallInteger, ForeignKey('cohort.id'), nullable=False)
    msg_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_updated = Column(DateTime, nullable=False, default=func.now())

    user = relationship('User', back_populates='bots')
    cohort = relationship('Cohort', back_populates='bots')


class Channel(Base):
    __tablename__ = 'channel'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(64), nullable=False)
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    cohort_id = Column(SmallInteger, ForeignKey('cohort.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_updated = Column(DateTime, nullable=False, default=func.now())

    user = relationship('User', back_populates='channels')
    cohort = relationship('Cohort', back_populates='channels')


class Cohort(Base):
    __tablename__ = 'cohort'
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    nickname = Column(String(16), nullable=False)
    duration = Column(SmallInteger, nullable=False)
    start_date = Column(Date, nullable=False)
    is_active = Column(Boolean, nullable=True)
    review_schema = Column(JSON, nullable=True)
    feedback_schema = Column(JSON, nullable=True)

    bots = relationship(
        'Bot', back_populates='cohort', order_by='Bot.created_at'
    )
    channels = relationship(
        'Channel', back_populates='cohort', order_by='Channel.created_at'
    )
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
        'User',
        foreign_keys=[evaluator_id],
        back_populates='evals_as_evaluator'
    )
    evaluatee = relationship(
        'User',
        foreign_keys=[evaluatee_id],
        back_populates='evals_as_evaluatee'
    )
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


class Subscription(Base):
    __tablename__ = 'subscription'
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    email = Column(String(64), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
