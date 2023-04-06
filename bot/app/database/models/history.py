from . import Base

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class History(Base):
    __tablename__ = 'history'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[BigInteger] = mapped_column()
    ad_id: Mapped[int] = mapped_column()
    time: Mapped[int] = mapped_column()
