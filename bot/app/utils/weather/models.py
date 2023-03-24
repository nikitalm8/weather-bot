from typing import List

from pydantic import BaseModel, Field


class WeatherType(BaseModel):
    
    id: int
    main: str
    description: str
    icon: str


class Coord(BaseModel):
    
    lon: float
    lat: float


class Main(BaseModel):
    
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int | None = None
    humidity: int | None = None
    sea_level: int | None = None
    grnd_level: int | None = None
    

class Wind(BaseModel):
    
    speed: float | None = None
    deg: int | None = None
    gust: float | None = None
    

class Rain(BaseModel):
    
    one_hour: float = Field(None, alias="1h")
    three_hours: float = Field(None, alias="3h")


class Snow(BaseModel):
    
    one_hour: float = Field(None, alias="1h")
    three_hours: float = Field(None, alias="3h")
    
    
class Clouds(BaseModel):
    
    all: int | None = None
    

class Sys(BaseModel):
    
    type: int
    id: int
    country: str
    sunrise: int
    sunset: int
    

class Weather(BaseModel):
    
    coord: Coord
    weather: List[WeatherType]
    base: str
    main: Main
    visibility: int
    wind: Wind
    rain: Rain | None = None
    snow: Snow | None = None
    clouds: Clouds
    dt: int
    sys: Sys
    timezone: int
    id: int
    name: str
    cod: int