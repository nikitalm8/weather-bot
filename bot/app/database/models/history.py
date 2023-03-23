from . import Base

from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
)


class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(BigInteger)
    ad_id = Column(Integer)
    time = Column(Integer)
