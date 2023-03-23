from . import Base

from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Boolean,
    Float,
)


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)

    join_date = Column(Integer)
    block_date = Column(Integer, default=0)

    ref = Column(String)
    subbed = Column(Boolean, default=False)
    subbed_before = Column(Boolean, default=False)
    
    latitude = Column(Float)
    longitude = Column(Float)
