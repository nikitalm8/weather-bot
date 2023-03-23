import asyncio
import logging

from app import (
    middlewares,
    handlers,
    utils,
)
from app.database import create_sessionmaker
from app.utils import set_commands, weather

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation


logger = logging.getLogger(__name__)

async def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger.info("Starting bot...")

    config = utils.load_config('config.yaml')

    if not config.debug:
    
        logging.getLogger("aiogram.event").setLevel(logging.WARNING)
    
    storage = MemoryStorage()
    sessionmaker = await create_sessionmaker(
        config.database_url, 
        debug=config.debug,
    )
    weather_api = weather.WeatherClient(config.weather_token)

    bot = Bot(
        token=config.token,
        parse_mode="HTML",
    )
    dp = Dispatcher(storage=storage, events_isolation=SimpleEventIsolation())

    middlewares.setup(dp, sessionmaker)
    handlers.setup(dp)

    await set_commands(bot, config)

    try:

        await dp.start_polling(bot, config=config, weather=weather_api)

    finally:

        await dp.fsm.storage.close()


try:

    asyncio.run(main())

except (
    KeyboardInterrupt,
    SystemExit,
):

    logger.info("Bot stopped")
