from PPlay.sprite import *

class Player:
    def __init__(self, x, y, image_path='imgs/ships/player.png'):
        self.sprite = Sprite(image_path)
        self.sprite.set_position(x, y)

    def draw(self):
        self.sprite.draw()

    def move(self, var_x, var_y):
        self.sprite.set_position(self.sprite.x + var_x, self.sprite.y + var_y)