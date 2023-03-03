#!/usr/bin/env python
import time
from train_api import train_estimates
from matrix_api import Matrix, Color

# print(train_estimates("Q", "Q03S"))
matrix = Matrix()

def draw():
    q_color = Color(255, 255, 0)
    matrix.drawText(0, 10, q_color, "Test")
    matrix.drawCircle(15, 15, 10, q_color)

def main():
    draw()
    time.sleep(5)

if __name__ == '__main__':
    main()
