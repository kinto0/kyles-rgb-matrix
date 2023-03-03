#!/usr/bin/env python
import time
import asyncio
from datetime import datetime, timedelta
from train_api import train_estimates
from matrix_api import Matrix, Color

matrix = Matrix()
q_color = Color(255, 205, 0)
six_color = Color(0, 147, 61)
text_color = Color(0, 211, 0)
no_color = Color(0, 0, 0)
seconds: int = 0
q_times = None
six_times = None

async def update_times():
    global q_times, six_times, seconds
    [q_times, six_times] = await asyncio.gather(train_estimates("Q", "Q03S"), train_estimates("6", "628S"))
    seconds = 0

def format_times(times) -> str:
    now = datetime.now()
    real_trains = list(filter(lambda x: x > now + timedelta(minutes=4), times))
    if len(real_trains) < 3:
        print("bad. train times empty")
    time_untils = [real_train - now for real_train in real_trains]
    return f'{time_untils[0].seconds // 60 :02d}:{time_untils[0].seconds % 60 :02d},{",".join([str(t.seconds // 60) for t in time_untils[1:3]])}'


async def draw():
    global seconds, scheduler, q_times, six_times
    seconds += 1

    # Draw recency line
    matrix.drawLine(0, 0, seconds * 2, 0, q_color)

    q_y = 5
    # Draw Q
    matrix.drawFilledCircle(4, q_y + 2, 4, q_color)
    matrix.drawText(3, q_y + 5, no_color, "Q")
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

    matrix.tick()

async def run_draw_loop():
    while True:
        await asyncio.gather(
                asyncio.sleep(1),
                draw()
        )

async def run_request_loop():
    while True:
        await asyncio.gather(
                asyncio.sleep(30),
                update_times()
        )
        
async def main():
    matrix.drawText(0, 10, text_color, "loading")
    matrix.tick()
    await update_times()

    await asyncio.gather(
        run_draw_loop(),
        run_request_loop()
    )

if __name__ == '__main__':
    asyncio.run(main())
