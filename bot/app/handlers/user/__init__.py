from . import (
    start,
    notsubbed,
    events,
    weather
)

from aiogram import Router, Dispatcher


def setup(dp: Dispatcher, router: Router):
    
    events.reg_handlers(dp)
    start.reg_handlers(router)
    
    notsubbed.reg_handlers(router)
    
    weather.reg_handlers(router)
