from . import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)


class Sponsor(Base):
    __tablename__ = 'sponsors'

    id = Column(Integer, primary_key=True, autoincrement=True)

    check = Column(Boolean, default=False)
    is_bot = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    title = Column(String)
    link = Column(String)
    access_id = Column(String)

    visits = Column(Integer, default=0)
    limit = Column(Integer, default=0)
