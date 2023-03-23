import time
import json
import random

from app.database.models import History, Advert

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, Update

from sqlalchemy import or_
from sqlalchemy.future import select


class AdMiddleware(BaseMiddleware):


    async def __call__(
        self, 
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        message: Message,
        data: Dict[str, Any],
    ) -> None:

        await handler(message, data)

        session = data['session']
        config = data['config']
        state = data['state']
 
        if (
            message.from_user.id in config.admins 
            or message.chat.type != 'private'
        ):

            return

        METHODS = (
            None,
            message.answer_photo,
            message.answer_video,
            message.answer_animation,
            message.answer_audio,
            message.answer_voice,
        )

        unix_time = time.time()
        state_data = await state.get_data()
        next_check = state_data.get(
            'next_ad_check', 0,
        )

        if next_check > unix_time:

            return

        confirm = await session.scalar(
            select(History).where(
                History.user_id == message.from_user.id,
                History.time > unix_time - 900,
            )
        )

        if confirm:

            return await state.update_data(
                next_ad_check=confirm.time + 900,
            )

        adverts = (await session.scalars(
            select(Advert).where(
                Advert.is_active,
                or_(
                    Advert.target == 0,
                    Advert.views < Advert.target,
                ),
                Advert.id.notin_(
                    select(History.ad_id).where(
                        History.user_id == message.from_user.id,
                    ),
                ),
            )
        )).all()

        if not adverts:

            return

        ad: Advert = random.choice(adverts)

        if ad.type == 0:

            await message.answer(
                ad.text,
                reply_markup=(
                    json.loads(ad.markup)
                    if ad.markup else None
                ),
                disable_web_page_preview=True,
                disable_notification=True,
            )

        else:

            await METHODS[ad.type](
                ad.file_id,
                caption=ad.text,
                reply_markup=(
                    json.loads(ad.markup)
                    if ad.markup else None
                ),
                disable_notification=True,
            )

        session.add(
            History(
                user_id=message.from_user.id,
                ad_id=ad.id,
                time=unix_time,
            ),
        )
        ad.views += 1

        await session.commit()
        await state.update_data(
            next_ad_check=unix_time + 900,
        )
