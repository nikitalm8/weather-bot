import sqlalchemy.orm as orm

from .user import UserMiddleware
from .callback import CallbackMiddleware
from .subscribe import SubMiddleware
from .adverts import AdMiddleware

from aiogram import Dispatcher


def setup(dp: Dispatcher, sessionmaker: orm.sessionmaker):

    dp.update.outer_middleware(UserMiddleware(sessionmaker))

    dp.message.outer_middleware(SubMiddleware())
    dp.callback_query.outer_middleware(SubMiddleware())

    dp.message.middleware(AdMiddleware())

    dp.callback_query.middleware(CallbackMiddleware())
