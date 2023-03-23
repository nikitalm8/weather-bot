from . import (
    admin,
    user,
)
from app.filters import IsAdmin

from aiogram import Dispatcher, Router


def setup(dp: Dispatcher):

    admin_router = Router() 

    admin_router.message.filter(IsAdmin())
    admin_router.callback_query.filter(IsAdmin())

    dp.include_router(admin_router)

    admin.setup(admin_router)

    user_router = Router()
    dp.include_router(user_router)

    user.setup(dp, user_router) # event handlers are registered for Dispatcher
