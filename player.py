from PPlay.sprite import *

class Player:
    def __init__(self, x, y, image_path='imgs/ships/player.png'):
        self.sprite = Sprite(image_path)

        player_x = x - self.sprite.width / 2
        player_y = y - self.sprite.height / 2
        
        self.sprite.set_position(player_x, player_y)

    def draw(self):
        self.sprite.draw()

    def move(self, var_x, var_y):
        self.sprite.set_position(self.sprite.x + var_x, self.sprite.y + var_y)

