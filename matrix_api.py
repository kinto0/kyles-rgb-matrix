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
        options.show_refresh_rate = 0
        options.rows = 32
        options.cols = 64
        options.drop_privileges = False
        options.brightness = 100
        options.hardware_mapping = "adafruit-hat"
        # options.limit_refresh_rate_hz = 60
        options.pwm_bits = 3

        self.matrix = RGBMatrix(options = options)
        self.canvas = self.matrix.CreateFrameCanvas()

    def drawText(self, x: int, y: int, color: Color, text: str):
        graphics.DrawText(self.canvas, font, x, y, graphics.Color(color.r, color.g, color.b), text)

    def drawCircle(self, x: int, y: int, radius: int, color: Color):
        graphics.DrawCircle(self.canvas, x, y, radius, graphics.Color(color.r, color.g, color.b))

    def drawFilledCircle(self, x: int, y: int, radius: int, color: Color):
        for x_diff in range(-radius, radius):
            y_diff = radius - abs(x_diff)
            graphics.DrawLine(
                    self.canvas,
                    x + x_diff,
                    y - y_diff,
                    x + x_diff,
                    y + y_diff,
                    graphics.Color(color.r, color.g, color.b)
                )

    def drawLine(self, x: int, y: int, x2: int, y2: int, color: Color):
        graphics.DrawLine(self.canvas, x, y, x2, y2, graphics.Color(color.r, color.g, color.b))

    def tick(self):
        self.canvas = self.matrix.SwapOnVSync(self.canvas)
        self.canvas.Clear()

