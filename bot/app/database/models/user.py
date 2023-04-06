from . import Base

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = 'users'

    id: Mapped[BigInteger] = mapped_column(primary_key=True, autoincrement=True)

    join_date: Mapped[int] = mapped_column()
    block_date: Mapped[int] = mapped_column(default=0)

    ref: Mapped[str] = mapped_column()
    subbed: Mapped[bool] = mapped_column(default=False)
    subbed_before: Mapped[bool] = mapped_column(default=False)
    
    latitude: Mapped[float] = mapped_column()
    longitude: Mapped[float] = mapped_column()
