from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.window import *
# from mouse import Mouse

class MenuOption:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.button = Sprite("imgs/button.png")
        self.button.set_position(x, y)
        self.mouse = Mouse()

    def draw(self, window):
        self.button.draw()
        text_size = int(self.button.height * 2 / 3)
        text_padding = int(self.button.height * 1 / 3 * 1 / 2)
        text_x = self.x + text_padding
        text_y = self.y + text_padding - 2
        window.draw_text(self.text, text_x, text_y, size=text_size, color=(0, 0, 0), font_name="arial")

    def clicked(self):
        return self.mouse.is_button_pressed(1) and self.mouse.is_over_object(self.button)
