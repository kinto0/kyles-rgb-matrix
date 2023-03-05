from dotenv import load_dotenv
from enum import Enum
import dataclasses
import httpx
import os
import json
from typing import Optional, List

load_dotenv()

@dataclasses.dataclass
class Weather:
    icon_paths: List[str] = dataclasses.field(default_factory=list)
    current: int = 0
    low: int = 0
    high: int = 0

def get_icon_paths(weather_id: int) -> List[str]:
    """weather ID from https://openweathermap.org/weather-conditions"""
    def paths(name: str):
        return [f'icons/{name}-0.png', f'icons/{name}-1.png']
   
    if weather_id < 300:
        return paths("lightning")
    elif weather_id < 600:
        return paths("rain")
    elif weather_id < 700:
        return paths("snow")
    elif weather_id < 801:
        return paths("sun")
    elif weather_id < 803:
        return paths("partially")
    else:
        return ["icons/cloudy.png"]

async def get_weather() -> Optional[Weather]:
    async with httpx.AsyncClient() as client:
        try:
            app_id = os.getenv("WEATHER_KEY")
            lat, lon = 40.77, -73.96
            r = await client.get(f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&appid={app_id}&units=imperial')
            content = json.loads(r.content)

            current = int(content['current']['temp'])
            low = int(content['daily'][0]['temp']['min'])
            high = int(content['daily'][0]['temp']['max'])
            icon_paths = get_icon_paths(content['daily'][0]['weather'][0]['id'])
            return Weather(icon_paths, current, low, high)
        except Exception as e:
            print(e)
            return None
 
