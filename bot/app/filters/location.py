from app.database.models import User

from aiogram.filters import Filter


class NoLocation(Filter):

    async def __call__(self, _, user: User) -> bool:

        return not (user.latitude and user.longitude)
