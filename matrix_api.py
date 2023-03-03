from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from dataclasses import dataclass

font = graphics.Font()
font.LoadFont("./tom-thumb.bdf")

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

    def drawFilledCircle(self, x: int, y: int, radius: int, color: Color):
        for x_diff in range(-radius, radius):
            y_diff = radius - abs(x_diff)
            graphics.DrawLine(
                    self.matrix,
                    x + x_diff,
                    y - y_diff,
                    x + x_diff,
                    y + y_diff,
                    graphics.Color(color.r, color.g, color.b)
                )

    def drawLine(self, x: int, y: int, x2: int, y2: int, color: Color):
        graphics.DrawLine(self.matrix, x, y, x2, y2, graphics.Color(color.r, color.g, color.b))

    def clear(self):
        self.matrix.Clear()

