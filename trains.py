#!/usr/bin/env python
import time
import asyncio
from datetime import datetime, timedelta
from train_api import TrainTimes
from matrix_api import Matrix, Color
from weather_api import get_weather, Weather
import signal, sys

matrix = Matrix()
q_color = Color(255, 205, 0)
six_color = Color(0, 147, 61)
text_color = Color(200, 200, 200)
no_color = Color(0, 0, 0)
half_seconds: int = 0
q_times = TrainTimes("Q", "Q03S")
six_times = TrainTimes("6", "628S")
current_weather = Weather()

tasks = {}

async def update_times():
    global q_times, six_times, half_seconds
    await asyncio.gather(q_times.refresh(), six_times.refresh())
    half_seconds = 0

def format_times(times) -> str:
    try:
        now = datetime.now()
        real_trains = list(filter(lambda x: x > now + timedelta(minutes=4), times.get_times()))
        if len(real_trains) < 3:
            print("bad. train times empty")
        time_untils = [real_train - now for real_train in real_trains]
        return f'{time_untils[0].seconds // 60 :02d}:{time_untils[0].seconds % 60 :02d},{",".join([str(t.seconds // 60) for t in time_untils[1:3]])}'
    except:
        return 'loading'


async def draw():
    global half_seconds, scheduler, q_times, six_times, current_weather
    half_seconds += 1

    # Draw recency line
    matrix.drawLine(0, 0, half_seconds, 0, q_color)

    q_y = 5
    # Draw Q
    matrix.drawFilledCircle(4, q_y + 2, 4, q_color)
    matrix.drawText(3, q_y + 5, no_color, "Q")
    matrix.drawFilledCircle(4, q_y + 5, 1, q_color)
    # Draw stop + down arrow
    matrix.drawText(9, q_y + 5, q_color, "72")
    matrix.drawLine(18, q_y, 18, q_y + 4, q_color)
    matrix.drawLine(17, q_y + 3, 19, q_y + 3, q_color)
    # Draw times
    matrix.drawText(21, q_y + 5, text_color, format_times(q_times))

    
    six_y = 15
    # Draw 6
    matrix.drawFilledCircle(4, six_y + 2, 4, six_color)
    matrix.drawText(3, six_y + 5, no_color, "6")
    # Draw stop + down arrow
    matrix.drawText(9, six_y + 5, six_color, "68")
    matrix.drawLine(18, six_y, 18, six_y + 4, six_color)
    matrix.drawLine(17, six_y + 3, 19, six_y + 3, six_color)
    # Draw times
    matrix.drawText(21, six_y + 5, text_color, format_times(six_times))
    
    weather_y = 25
    # Draw weather
    matrix.drawText(4, weather_y + 5, text_color, f'{current_weather.current}°, {current_weather.condition}. {current_weather.low}-{current_weather.high}')

    matrix.tick()

async def run_draw_loop():
    global tasks
    while True:
        tasks['draw'] = asyncio.gather(
                asyncio.sleep(.5),
                draw()
        )
        await tasks['draw']

async def run_request_loop():
    while True:
        tasks['trains'] = asyncio.gather(
                asyncio.sleep(30),
                update_times()
        )
        await tasks['trains']

async def run_weather_loop():
    global current_weather
    async def update_weather():
        current_weather = await get_weather()
    while True:
        tasks['weather'] = asyncio.gather(
                asyncio.sleep(3600),
                update_weather()
        )
        await tasks['weather']

def exit_gracefully(sig, frame):
    global matrix, tasks
    print("exiting")
    [task.cancel() for _, task in tasks.items()]
    matrix.tick()
    sys.exit(0)
    
async def main():
    global matrix, text_color

    signal.signal(signal.SIGINT, exit_gracefully)
    matrix.drawText(0, 10, text_color, "loading")
    matrix.tick()

    await asyncio.gather(
        run_draw_loop(),
        run_request_loop(),
        run_weather_loop()
    )

if __name__ == '__main__':
    asyncio.run(main())
