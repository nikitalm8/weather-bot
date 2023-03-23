from app.filters import NotSubbed
from app.templates import texts
from app.templates.keyboards import user as nav
from app.database.models import User, Sponsor

from contextlib import suppress

from aiogram import Router, types, exceptions
from aiogram.filters import Text

from sqlalchemy import update


async def notsubbed(message: types.Message, sponsors: list, session, user: User):

    await message.answer(
        texts.user.NOT_SUBBED,
        reply_markup=nav.inline.subscription(
            sponsors,
        )
    )

    if user.subbed:

        user.subbed = False
        await session.commit()
        

async def notsubbed_cb(call: types.CallbackQuery, sponsors: list, session, user: User):

    await call.answer(
        'Вы не подписаны на одного из спонсоров.'
    )

    with suppress(exceptions.TelegramAPIError):

        await call.message.edit_text(
            texts.user.NOT_SUBBED,
            reply_markup=nav.inline.subscription(
                sponsors,
            )
        )

    if user.subbed:

        user.subbed = False
        await session.commit()


async def subbed(call: types.CallbackQuery, session, user: User):

    await call.message.edit_text(
        texts.user.SUBBED,
    )

    if user.subbed_before and user.subbed:

        return

    user.subbed = True
    
    if not user.subbed_before:

        user.subbed_before = True

        await session.execute(
            update(Sponsor)
            .where(Sponsor.is_active == True)
            .values(visits = Sponsor.visits + 1)
        )
        await session.execute(
            update(Sponsor)
            .where(Sponsor.limit != 0, Sponsor.visits >= Sponsor.limit)
            .values(is_active = False)
        )

    await session.commit()


def reg_handlers(router: Router):

    router.message.register(notsubbed, NotSubbed())
    router.callback_query.register(notsubbed_cb, NotSubbed())

    router.callback_query.register(subbed, Text("checksub"))
