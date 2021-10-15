from flask_login import UserMixin
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    func,
    SmallInteger,
    String
)
from sqlalchemy.orm import relationship

from database import Base


class User(UserMixin, Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    password = Column(String(60), nullable=False)
    name = Column(String(64), nullable=False)
    discriminator = Column(String(4), nullable=False)
    display_name = Column(String(64), nullable=False)
    cohort_id = Column(SmallInteger, ForeignKey('cohort.id'), nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_updated = Column(DateTime, nullable=False, default=func.now())

    cohort = relationship('Cohort', back_populates='user')


class Cohort(Base):
    __tablename__ = 'cohort'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(64), nullable=False)
    duration = Column(SmallInteger, nullable=False)
    start_date = Column(DateTime, nullable=False)

    user = relationship('User', back_populates='cohort')
