from . import (
    dump,
    start,
    stats,
    referrals,
    subscribe,
    mail,
    adverts,
)

from aiogram import Router


def setup(router: Router):

    start.reg_handlers(router)
    dump.reg_handlers(router)
    mail.reg_handlers(router)
    stats.reg_handlers(router)
    referrals.reg_handlers(router)
    subscribe.reg_handlers(router)
    adverts.reg_handlers(router)
