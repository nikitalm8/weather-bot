from . import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)


class Advert(Base):
    __tablename__ = 'adverts'

    id = Column(Integer, primary_key=True, autoincrement=True)

    type = Column(Integer)
    title = Column(String)
    text = Column(String)
    file_id = Column(String)
    markup = Column(String)

    views = Column(Integer, default=0)
    target = Column(Integer)
    is_active = Column(Boolean, default=True)
