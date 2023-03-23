import time

from app.database.models import User, Sponsor

from typing import Any, Awaitable, Callable, Dict
from contextlib import suppress

from aiogram import BaseMiddleware, Bot, exceptions
from aiogram.types import Update

from sqlalchemy.future import select


class SubMiddleware(BaseMiddleware):


    async def __call__(
        self, 
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:

        user: User = data['user']
        session = data['session']
        config = data['config']
        state = data['state']

        chat = data.get('event_chat')

        if not chat or user.id in config.admins:

            data['sponsors'] = []
            return await handler(event, data)
            
        last_check = (await state.get_data()).get('last_check', 0)
        have_to_check = (
            last_check < (time.time() - 60)
            and chat.type == 'private'
        )
        available_sponsors = []

        if have_to_check:

            sponsors = await session.scalars(
                select(Sponsor)
                .where(Sponsor.is_active == True)
            )

            available_sponsors = await self.get_sponsors(sponsors, user, data['bot'])

            if not available_sponsors:
                       
                await state.update_data(
                    last_check=time.time(),
                )

        data['sponsors'] = available_sponsors

        return await handler(event, data)


    @classmethod
    async def get_sponsors(cls, sponsors: list[Sponsor], user: User, bot: Bot) -> list:

        not_subbed = []
        no_check = []

        for sponsor in sponsors:

            if not sponsor.check:

                no_check.append(sponsor)

            elif await cls.not_sub(sponsor, user, bot):

                not_subbed.append(sponsor)

        if bool(not_subbed):

            return no_check + not_subbed


    @staticmethod
    async def not_sub(sponsor: Sponsor, user: User, bot: Bot) -> bool:

        if sponsor.is_bot:
            
            try:

                _bot = Bot(sponsor.access_id, session=bot.session)
                await _bot.send_chat_action(user.id, 'typing')
            
            except (
                exceptions.TelegramNotFound,
                exceptions.TelegramBadRequest,
                exceptions.TelegramForbiddenError,
            ):
            
                return True

        else:

            with suppress(exceptions.TelegramAPIError):

                member = await bot.get_chat_member(
                    sponsor.access_id,
                    user.id,
                )

                if member.status in ('left', 'kicked', None):

                    return True

        return False
