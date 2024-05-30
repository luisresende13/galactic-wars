from PPlay.sprite import *

class Shot:
    def __init__(self, x, y, x_dir=0, y_dir=-1, image_path='imgs/shots/shot-fire-1.png'):
        self.x = x
        self.y = y
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.sprite = Sprite(image_path)

        sprite_x = x - self.sprite.width / 2
        sprite_y = y - self.sprite.height / 2
        
        self.sprite.set_position(sprite_x, sprite_y)

    def draw(self):
        self.sprite.draw()

    def move(self, var_x, var_y):
        self.sprite.set_position(self.sprite.x + var_x, self.sprite.y + var_y)
