from aiogram.filters import Filter


class NotSubbed(Filter):

    async def __call__(self, _, sponsors: list):

        return bool(sponsors)
