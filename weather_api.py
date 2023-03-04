from dotenv import load_dotenv
from enum import Enum
import dataclasses
import httpx
import os
import json
from typing import Optional, List

load_dotenv()

content = json.loads("""{
  "lat": 39.31,
  "lon": -74.5,
  "timezone": "America/New_York",
  "timezone_offset": -18000,
  "current": {
    "dt": 1646318698,
    "sunrise": 1646306882,
    "sunset": 1646347929,
    "temp": 28.21,
    "feels_like": 278.41,
    "pressure": 1014,
    "humidity": 65,
    "dew_point": 275.99,
    "uvi": 2.55,
    "clouds": 40,
    "visibility": 10000,
    "wind_speed": 8.75,
    "wind_deg": 360,
    "wind_gust": 13.89,
    "weather": [
      {
        "id": 802,
        "main": "Clouds",
        "description": "scattered clouds",
        "icon": "03d"
      }
    ]
  },
    "daily": [
    {
      "dt": 1646326800,
      "sunrise": 1646306882,
      "sunset": 1646347929,
      "moonrise": 1646309880,
      "moonset": 1646352120,
      "moon_phase": 0.03,
      "temp": {
        "day": 281.63,
        "min": 27.72,
        "max": 28.21,
        "night": 271.72,
        "eve": 277.99,
        "morn": 280.92
      },
      "feels_like": {
        "day": 277.83,
        "night": 264.72,
        "eve": 273.35,
        "morn": 277.66
      },
      "pressure": 1016,
      "humidity": 55,
      "dew_point": 273.12,
      "wind_speed": 9.29,
      "wind_deg": 3,
      "wind_gust": 16.48,
      "weather": [
        {
          "id": 500,
          "main": "Rain",
          "description": "light rain",
          "icon": "10d"
        }
      ],
      "clouds": 49,
      "pop": 0.25,
      "rain": 0.11,
      "uvi": 3.38
    }]
    }""")

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
            lat, lon = 40.77, 73.96
            #r = await client.get(f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&appid={app_id}&units=imperial')
            #content = json.loads(r.content)

            global content
            current = content['current']['temp']
            low = content['daily'][0]['temp']['min']
            high = content['daily'][0]['temp']['max']
            # condition = content['daily'][0]['weather'][0]['description']
            return Weather(["icons/cloudy-0.png", "icons/cloudy-1.png"], current, low, high)
        except Exception as e:
            print(e)
            return None
 
