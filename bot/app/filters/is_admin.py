from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery


class IsAdmin(Filter):

    def __init__(self, is_admin: bool=True):

        self.is_admin = is_admin

    async def __call__(self, update: Message | CallbackQuery, config):

        return self.is_admin == (
            update.from_user.id 
            in config.admins
        )
