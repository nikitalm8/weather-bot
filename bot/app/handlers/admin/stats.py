from app.database.models import User
from app.templates import texts
from app.utils import get_times, plots

from aiogram import Router, types
from aiogram.filters import Text, Command

from sqlalchemy import func
from sqlalchemy.future import select


async def user_stats(message: types.Message, session) -> None:

    statements = (
        select(func.count(User.id)),
        select(func.count(User.id)).where(User.block_date == 0),
        select(func.count(User.id)).where(User.block_date != 0),
        select(func.count(User.id)).where(User.subbed == True),
        *(
            select(func.count(User.id)).where(User.join_date >= date)
            for date in get_times()
        ),
    )

    results = [
        await session.scalar(stmt)
        for stmt in statements
    ]

    text = texts.admin.STATS % tuple(results)
    msg = await message.answer_animation(
        'https://media.tenor.com/kOosNeYUmWkAAAAC/loading-buffering.gif', 
        caption=text,
    )
    image = await plots.UsersPlot.create_plot(session)

    await msg.edit_media(
        types.InputMediaPhoto(
            media=types.FSInputFile(image), 
            caption=text,
        )
    )
    

def reg_handlers(router: Router):

    router.message.register(user_stats, Text("Статистика"))
    router.message.register(user_stats, Command("stats"))
