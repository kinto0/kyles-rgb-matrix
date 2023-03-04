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
            # condition = content['daily'][0]['weather'][0]['description']
            return Weather(["icons/cloudy-0.png", "icons/cloudy-1.png"], current, low, high)
        except Exception as e:
            print(e)
            return None
 
