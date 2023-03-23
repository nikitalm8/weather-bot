from app.templates.keyboards import admin as nav
from app.database.models import User

from aiogram import Router, types
from aiogram.filters import Command, Text
from sqlalchemy.future import select


async def get_users(call: types.CallbackQuery, session, select_alive: bool=False) -> None:

    FILE_PATH = "app/src/users.txt"

    stmt = select(User.id)
    
    if select_alive:

        stmt = stmt.where(User.block_date == 0)

    users = (await session.scalars(stmt)).all()

    with open(FILE_PATH, "w") as file:

        file.write(
            "\n".join([
                str(user) 
                for user in users
            ])
        )

    await call.message.answer_document(
        types.FSInputFile(FILE_PATH),
        caption=f"Выгружено пользователей: {len(users)}",
    )
    await call.message.delete()


async def dump_users(call: types.CallbackQuery, session) -> None:

    action = call.data.split(":")[1]
    await get_users(
        call, 
        session,
        select_alive=(action == "alive")
    )


async def pre_dump_users(message: types.Message) -> None:

    await message.answer(
        "Каких пользователей выгрузить?",
        reply_markup=nav.inline.DUMP,
    )


def reg_handlers(router: Router):

    router.message.register(pre_dump_users, Command("dump"))
    router.message.register(pre_dump_users, Text("Выгрузка"))

    router.callback_query.register(dump_users, Text(startswith="dump"))
