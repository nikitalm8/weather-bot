from app.filters import NoLocation
from app.utils.weather import WeatherClient
from app.database.models import User

from app.templates import texts
from app.templates.keyboards import user as nav

from contextlib import suppress
from cachetools import TTLCache

from aiogram import Router, types, exceptions
from aiogram.filters import Text, command


WEATHER_CACHE = TTLCache(
    maxsize=100, ttl=60 * 5,
)


async def get_weather(lat: float, lon: float, weather: WeatherClient):

    index = '%s:%s' % (lat, lon)

    if not (current_weather := WEATHER_CACHE.get(index)):
        
        current_weather = await weather.get_weather(lat, lon)    
        WEATHER_CACHE[index] = current_weather
        
    return current_weather


async def send_weather(
    update: types.Message | types.CallbackQuery, 
    weather: WeatherClient, 
    lat: float, 
    lon: float,
    reply_markup: dict | None=None,
):
    
    current_weather = await get_weather(lat, lon, weather)    
    method = (
        update.answer if isinstance(update, types.Message) 
        else update.message.edit_text
    )

    with suppress(exceptions.TelegramBadRequest):

        await method(
            texts.user.weather_text(current_weather),
            reply_markup=reply_markup or nav.inline.WEATHER,
        )  


async def user_weather(
    update: types.Message | types.CallbackQuery, 
    user: User, weather: WeatherClient
):
    
    await send_weather(
        update, weather, 
        user.latitude, user.longitude,
    )


async def popular_places(update: types.Message | types.CallbackQuery, config):
    
    method = (
        update.answer if isinstance(update, types.Message) 
        else update.message.edit_text
    )
    await method(
        texts.user.POPULAR_PLACES,
        reply_markup=nav.inline.popular_places(config.popular_places),
    )
    
    
async def place_weather(call: types.CallbackQuery, config, weather: WeatherClient):
    
    place_id = int(call.data.split(':')[1])
    place = config.popular_places[place_id]
    
    await send_weather(
        call, weather, 
        place['latitude'], place['longitude'],
        reply_markup=nav.inline.back(place_id),
    )


async def inline_share(query: types.InlineQuery, user: User, weather: WeatherClient, config):
    
    if query.query.startswith('place:'):
        
        place_id = query.query.split(':')[1]
        
        try:
        
            place = config.popular_places[int(place_id)]
            lat, lon = place['latitude'], place['longitude']
            
        except (IndexError, ValueError):
            
            return
        
    else:
        
        if not (user.latitude and user.longitude):
            
            return await query.answer(
                results=[],
                switch_pm_text='Активировать бота',
                switch_pm_parameter='true',
            )
        
        lat, lon = user.latitude, user.longitude
    
    current_weather = await get_weather(lat, lon, weather)
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id=query.id,
                title='Поделиться погодой в г. %s ⛅' % current_weather.name,
                description='Жми, чтобы поделиться погодой в текущем чате',
                thumb_url='https://i.imgur.com/G5Q9oro.png',
                input_message_content=types.InputTextMessageContent(
                    message_text=texts.user.weather_text(current_weather),
                ),
            ),
        ],
    )
                    


def reg_handlers(router: Router):

    router.message.register(user_weather, Text('Погода ☀️'))
    router.callback_query.register(user_weather, Text('myweather'))
    
    router.message.register(popular_places, Text('Популярные места 🏙'))
    router.callback_query.register(popular_places, Text('back'))
    
    router.callback_query.register(place_weather, Text(startswith='weather:'))
    
    router.inline_query.register(inline_share)
