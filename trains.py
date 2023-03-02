#!/usr/bin/env python
import time
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions

options = RGBMatrixOptions()
options.show_refresh_rate = 1
options.rows = 32
options.cols = 64
options.drop_privileges = False
matrix = RGBMatrix(options = options)

font = graphics.Font()
font.LoadFont("./7x13.bdf")

def draw():
    graphics.DrawText(matrix, font, 0, 10, graphics.Color(0, 0, 255), "Test")
    graphics.DrawCircle(matrix, 15, 15, 10, graphics.Color(255, 0, 255))

def main():
    draw()
    time.sleep(1)
    options.brightness = 80
    matrix = RGBMatrix(options = options)
    draw()
    time.sleep(10)

if __name__ == '__main__':
    main()
