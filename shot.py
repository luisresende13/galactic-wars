from PPlay.sprite import *

class Shot:
    def __init__(self, x, y, image_path='imgs/shots/shot-fire-1.png'):
        self.x = x
        self.y = y
        self.sprite = Sprite(image_path)

        sprite_x = x - self.sprite.width / 2
        sprite_y = y - self.sprite.height / 2
        
        self.sprite.set_position(sprite_x, sprite_y)

    def draw(self):
        self.sprite.draw()

