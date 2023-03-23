from app.templates.keyboards import user, admin

from contextlib import suppress

from aiogram import Bot, exceptions
from aiogram.types import BotCommandScopeChat


async def set_commands(bot: Bot, config):

    await bot.set_my_commands(
        user.commands.user_commands,
    )

    for chat_id in config.admins:

        with suppress(exceptions.TelegramBadRequest):

            await bot.set_my_commands(
                admin.commands.admin_commands + user.commands.user_commands[1:], # user_commands[1:] - remove /start command
                scope=BotCommandScopeChat(chat_id=chat_id)
            )
