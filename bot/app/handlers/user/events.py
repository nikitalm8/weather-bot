import time

from app.database.models import User

from aiogram import Bot, Dispatcher, types

from sqlalchemy.ext.asyncio import AsyncSession


async def block_user(update: types.ChatMemberUpdated, user: User, session: AsyncSession):

    if update.new_chat_member.status in ("left", "kicked", None):

        user.block_date = time.time()
        await session.commit()

    elif user.block_date != 0:

        user.block_date = 0
        await session.commit()


async def chat_join_request(update: types.ChatJoinRequest, bot: Bot):

    try:

        await bot.send_message(
            update.from_user.id,
            "Привет!",
        )

    finally:

        await update.approve()


def reg_handlers(dp: Dispatcher):

    dp.my_chat_member.register(block_user)
    dp.chat_join_request.register(chat_join_request)
