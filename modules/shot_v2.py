import math
from PPlay.sprite import *
from modules.game_math import calculate_horizontal_vertical_distances

class Shot:
    def __init__(self, x_dir, y_dir, speed, image_path):
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.sprite = Sprite(image_path)
        self.speed = speed

    def draw(self):
        self.sprite.draw()

    def move(self, var_x, var_y):
        self.sprite.set_position(self.sprite.x + var_x, self.sprite.y + var_y)

    def auto_move(self, delta_time):
        distance = self.speed * delta_time
        angle_rad = math.atan2(self.y_dir, self.x_dir)
        delta_x, delta_y = calculate_horizontal_vertical_distances(distance, angle_rad)
        self.move(delta_x, delta_y)
