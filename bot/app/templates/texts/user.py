from app.utils.weather import Weather

from datetime import datetime


def weather_text(weather: Weather):
    
    return WEATHER_TEMPLATE % (
        weather.name,
        weather.weather[0].description,
        weather.main.temp,
        weather.main.feels_like,
        weather.wind.speed,
        datetime.fromtimestamp(
            weather.sys.sunrise,
        ).strftime('%H:%M'),
        datetime.fromtimestamp(
            weather.sys.sunset,
        ).strftime('%H:%M'),
    )


START = '''
Привет! 👋 
Я помогу тебе узнать погоду в любом городе.
<i>Обрати внимание, что данные о погоде кэшируются и обновляются раз в 5 минут.</i>
'''

WEATHER_TEMPLATE = '''
🌥️ <b>В г. %s сейчас %s</b>

🌡️ <b>Температура:</b> %s°C
<i>Ощущается как %s°C</i>

💨 <b>Ветер:</b> %s м/с
🌄 <b>Восход:</b> %s
🌆 <b>Закат:</b> %s
'''
POPULAR_PLACES = '⛅ Погода в популярных городах'

NOT_REGISTERED = '<i>Для использования бота необходимо поделиться своим местоположением 📍</i>'
LOCATION_UPDATED = 'Местоположение установлено 📍'

NOT_SUBBED = 'Ты не подписан на канал'
SUBBED = 'Ты подписан на канал'
