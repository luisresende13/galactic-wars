import math
from PPlay.sprite import *
from modules.game_math import calculate_horizontal_vertical_distances

class Shot:
    def __init__(self, x_dir, y_dir, speed, damage, image_path, shooter_id=None):
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.sprite = Sprite(image_path)
        self.speed = speed
        self.speed_x = 0
        self.speed_y = 0
        self.damage = damage
        self.shooter_id = shooter_id

    def draw(self):
        self.sprite.draw()

    def move(self, var_x, var_y):
        self.sprite.set_position(self.sprite.x + var_x, self.sprite.y + var_y)

    def auto_move(self, delta_time, delta_speed=0):
        distance = self.speed * delta_time
        angle_rad = math.atan2(self.y_dir, self.x_dir)
        delta_x, delta_y = calculate_horizontal_vertical_distances(distance, angle_rad)
        self.move(delta_x, delta_y)

        self.speed_x = delta_x / delta_time
        self.speed_y = delta_y / delta_time
