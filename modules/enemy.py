from PPlay.sprite import *


# def enemy_row(n, image_path, y=None):
#     enemy_ = Enemy(0, 0, 'imgs/ships/enemy-2-60x58.png')    
#     enemies = []
#     for i in range(n):
#         x = (i + 2) * enemy_.sprite.width / 2 + i * enemy_.sprite.width
#         # y = (j + 2) * enemy_.sprite.height / 2 + j * enemy_.sprite.height

#         enemy = Enemy(x, y, image_path)
 
#         enemies.append(enemy)
    
#     return monsters

class Enemy:
    def __init__(self, x, y, speed, image_path):
        self.speed = speed
        self.sprite = Sprite(image_path)
        self.sprite.set_position(x, y)

    def draw(self):
        self.sprite.draw()

    def move(self, var_x, var_y):
        self.sprite.set_position(self.sprite.x + var_x, self.sprite.y + var_y)

        