from . import Base

from sqlalchemy.orm import Mapped, mapped_column


class Advert(Base):
    __tablename__ = 'adverts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    type: Mapped[int] = mapped_column()
    title: Mapped[str] = mapped_column()
    text: Mapped[str] = mapped_column()
    file_id: Mapped[str] = mapped_column()
    markup: Mapped[str] = mapped_column()

    views: Mapped[int] = mapped_column(default=0)
    target: Mapped[int] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
