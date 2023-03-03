from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from dataclasses import dataclass

font = graphics.Font()
font.LoadFont("./7x13.bdf")

@dataclass
class Color:
    r: int
    g: int
    b: int

class Matrix:
    def __init__(self):
        options = RGBMatrixOptions()
        options.show_refresh_rate = 1
        options.rows = 32
        options.cols = 64
        options.drop_privileges = False

        self.matrix = RGBMatrix(options = options)

    def drawText(self, x: int, y: int, color: Color, text: str):
        graphics.DrawText(self.matrix, font, x, y, graphics.Color(color.r, color.g, color.b), text)

    def drawCircle(self, x: int, y: int, radius: int, color: Color):
        graphics.DrawCircle(self.matrix, x, y, radius, graphics.Color(color.r, color.g, color.b))

