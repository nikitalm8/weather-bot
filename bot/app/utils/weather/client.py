import aiohttp

from .models import Weather


class WeatherClient(object):
    
    API_URL = 'https://api.openweathermap.org/data/2.5/weather'
    
    def __init__(self, token: str) -> None:
        """
        Create an API instance.

        :param str token: API token
        """
        
        self.token = token
        self.session = aiohttp.ClientSession()
        
        
    async def get_weather(
        self, 
        lat: float, 
        lon: float, 
        units: str='metric',
        lang: str='ru',
    ) -> Weather:
        """
        Get current weather data.

        :param float lat: Latitude
        :param float lon: Longitude
        :param str units: Units
        :param str lang: Language
        :return Weather: Weather data
        """
        
        async with self.session.get(
            self.API_URL,
            params={
                'lat': lat,
                'lon': lon,
                'units': units,
                'appid': self.token,
                'lang': lang,
            },
        ) as response:
            
            data = await response.json()
            return Weather(**data)
