import time

from app.database.models import User

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import async_sessionmaker


class UserMiddleware(BaseMiddleware):
    

    def __init__(self, sessionmaker: async_sessionmaker):

        self.sessionmaker = sessionmaker


    async def __call__(
        self, 
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
    
        async with self.sessionmaker() as session:

            event_user = data.get("event_from_user")

            # if event has no user, don't fetch user from database
            if not event_user:

                return await handler(event, data)

            user = await session.scalar(
                select(User)
                .where(User.id == event_user.id)
            )

            if not user:

                ref = None
                
                if event.message and event.message.text:

                    split_text = event.message.text.split()[1:]

                    if split_text and split_text[0] == '/start':

                        ref = split_text[0]

                user = User(
                    id=event_user.id,
                    join_date=time.time(),
                    ref=ref,
                )
                session.add(user)
                await session.commit()

            data["user"] = user
            data["session"] = session

            return await handler(event, data)
