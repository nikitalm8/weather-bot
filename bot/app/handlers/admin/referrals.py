from math import ceil

from app.utils import get_times
from app.templates import texts
from app.templates.keyboards import admin as nav
from app.database.models import User

from aiogram import Router, types
from aiogram.filters import Command, Text

from sqlalchemy import update, func
from sqlalchemy.future import select


async def get_ref_info(session, ref_id, bot):

    statements = (
        select(func.count(User.id)).where(User.ref == ref_id),
        select(func.count(User.id)).where(User.ref == ref_id).where(User.block_date == 0),
        select(func.count(User.id)).where(User.ref == ref_id).where(User.subbed == True),
        *(
            select(func.count(User.id)).where(User.ref == ref_id).where(User.join_date >= date)
            for date in get_times()
        ),
    )

    return [
        ref_id,
        *[
            await session.scalar(stmt)
            for stmt in statements
        ],
        (await bot.me()).username,
    ]


async def get_refs(session) -> list[str]:

    refs = await session.scalars(
        select(User.ref.distinct())
        .where(User.ref != None)
    )

    return refs.all()


async def referral(message: types.Message, session):

    await message.answer(
        texts.admin.REF_LIST,
        reply_markup=nav.inline.ref_list(
            await get_refs(session),
        )
    )


async def ref_list(call: types.CallbackQuery, session, page: int=None):

    page = page or int(call.data.split(':')[1])
    refs = await get_refs(session)

    if page < 1 or page > ceil(len(refs)/9):

        return

    await call.message.edit_text(
        texts.admin.REF_LIST,
        reply_markup=nav.inline.ref_list(refs, page),
    )


async def ref(call: types.CallbackQuery, session, bot) -> None:

    action, ref = call.data.split(':')[1:]

    if action == 'info':

        await call.message.edit_text(
            texts.admin.REF.format(*await get_ref_info(session, ref, bot)),
            reply_markup=nav.inline.ref(ref),
        )

    elif action == 'del':

        await call.message.edit_text(
            texts.admin.REF_DEL % ref,
            reply_markup=nav.inline.choice(ref, 'ref'),
        )

    elif action == 'del2':

        await session.execute(
            update(User)
            .where(User.ref == ref)
            .values(ref=None)
        )
        await session.commit()

        await call.message.edit_text(
            texts.admin.REF_LIST,
            reply_markup=nav.inline.ref_list(
                await get_refs(session),
            )
        )

    elif action == 'list':

        await ref_list(call.message, session, page=1)


def reg_handlers(router: Router):

    router.message.register(referral, Command("referrals"))
    router.message.register(referral, Text("Рефералы"))

    router.callback_query.register(ref, Text(startswith="ref:"))
    router.callback_query.register(ref_list, Text(startswith="reflist"))
