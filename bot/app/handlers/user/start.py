
from app.database.models import User
from app.filters import NoLocation, ContentTypes
from app.templates import texts
from app.templates.keyboards import user as nav

from aiogram import Router, types
from aiogram.filters import CommandStart

from sqlalchemy.ext.asyncio import AsyncSession


async def start(message: types.Message):

    await message.answer(
        texts.user.START,
        reply_markup=nav.reply.MENU,
    )


async def no_reg(message: types.Message):

    await message.answer(
        texts.user.NOT_REGISTERED,
        reply_markup=nav.reply.LOCATION_REQUEST,
    )
    
    
async def update_location(message: types.Message, user: User, session: AsyncSession):

    user.latitude = message.location.latitude
    user.longitude = message.location.longitude
    await session.commit()

    await message.answer(
        texts.user.LOCATION_UPDATED,
        reply_markup=nav.reply.MENU,
    )


def reg_handlers(router: Router):
    
    router.message.register(update_location, ContentTypes(types.ContentType.LOCATION))
    router.message.register(no_reg, NoLocation())
    router.message.register(start, CommandStart())
