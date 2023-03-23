import asyncio

from app.filters import ContentTypes
from app.utils.mailing import MailerSingleton
from app.database.models import User
from app.templates.keyboards import admin as nav

from sqlalchemy.future import select

from aiogram import Router, types
from aiogram.filters import Text, Command, StateFilter
from aiogram.fsm.context import FSMContext

async def pre_mailing(message: types.Message, state: FSMContext) -> None:
    
    await message.answer(
        "Что вы хотите отправить?",
        reply_markup=nav.inline.CANCEL,
    )
    await state.set_state("mailing.text")


async def mailing_text(message: types.Message, state: FSMContext) -> None:

    await state.update_data(message=message)

    await message.copy_to(
        message.from_user.id,
        reply_markup=message.reply_markup,
    )
    await message.answer(
        "Начинаю рассылку?",
        reply_markup=nav.reply.CONFIRM,
    )

    await state.set_state("mailing.confirm")


async def mailing_confirm(message: types.Message, state: FSMContext, session) -> None:

    if message.text == 'Подтвердить':

        data = await state.get_data()
        scope = (await session.scalars(
            select(User.id).where(User.block_date == 0)
        )).all()

        await message.answer(
            'Начинаю рассылку...',
            reply_markup=nav.reply.MENU,
        )

        mailer = MailerSingleton.get_instance()
        asyncio.create_task(mailer.start_mailing(
            data['message'],
            scope,
            cancel_keyboard=nav.inline.STOPMAIL,
        ))

    else:

        await message.answer("Рассылка отменена.", reply_markup=nav.reply.MENU)
        await state.clear()


async def stop_mailing(call: types.CallbackQuery) -> None:

    MailerSingleton.get_instance().stop_mailing()
    
    await call.message.delete()
    await call.answer("Рассылка остановлена.")


async def cancel_mailing(call: types.CallbackQuery, state: FSMContext) -> None:

    await state.clear()

    await call.message.delete()
    await call.answer("Отменено.")


def reg_handlers(router: Router):

    router.message.register(pre_mailing, Command("mailing"))
    router.message.register(pre_mailing, Text("Рассылка"))

    router.message.register(mailing_text, StateFilter("mailing.text"), ContentTypes(types.ContentType.ANY))
    router.callback_query.register(cancel_mailing, Text("cancel"), StateFilter("mailing.text"))

    router.message.register(mailing_confirm, StateFilter("mailing.confirm"))

    router.callback_query.register(stop_mailing, Text("stopmail"))
    