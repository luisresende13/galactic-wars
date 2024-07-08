from PPlay.sprite import Sprite
from PPlay.window import Window

class Player:
    def __init__(self, acceleration, speed_x_max, speed_y_max):
        self.sprite = Sprite('imgs/ships/player/final/rotation/0.png')
        self.keyboard = Window.get_keyboard()
        
        self.acceleration = acceleration
        self.speed_x_max = speed_x_max
        self.speed_y_max = speed_y_max

        self.speed_x = 0
        self.speed_y = 0

    def draw(self):
        self.sprite.draw()

    def move(self, delta_x, delta_y):
        self.sprite.set_position(self.sprite.x + delta_x, self.sprite.y + delta_y)

    def accelerate(self):

        x_dir = 0
        y_dir = 0

        image_path = None
        if self.keyboard.key_pressed("D"):
            x_dir += + 1
            image_path = 'imgs/ships/player/final/rotation/90.png'
                
        if self.keyboard.key_pressed("A"):
            x_dir += - 1
            image_path = 'imgs/ships/player/final/rotation/270.png'

        if self.keyboard.key_pressed("S"):
            y_dir += + 1
            image_path = 'imgs/ships/player/final/rotation/180.png'

        if self.keyboard.key_pressed("W"):
            y_dir += - 1
            image_path = 'imgs/ships/player/final/rotation/0.png'

        if all([self.keyboard.key_pressed(key) for key in ("A", "W")]):
            image_path = 'imgs/ships/player/final/rotation/315.png'

        if all([self.keyboard.key_pressed(key) for key in ("A", "S")]):
            image_path = 'imgs/ships/player/final/rotation/225.png'
        
        if all([self.keyboard.key_pressed(key) for key in ("D", "W")]):
            image_path = 'imgs/ships/player/final/rotation/45.png'
        
        if all([self.keyboard.key_pressed(key) for key in ("D", "S")]):
            image_path = 'imgs/ships/player/final/rotation/135.png'

        # Rotate player with new angle
        if image_path is not None:
            x = self.sprite.x
            y = self.sprite.y
            self.sprite = Sprite(image_path)
            self.sprite.set_position(x, y)
            
        # Update player speed
        speed_x = self.speed_x + x_dir * self.acceleration
        speed_y = self.speed_y + y_dir * self.acceleration

        if speed_x >= 0:
            self.speed_x = min(speed_x, self.speed_x_max)
        else:
            self.speed_x = max(speed_x,  - 1 * self.speed_x_max)
            
        if speed_y >= 0:
            self.speed_y = min(speed_y, self.speed_y_max)
        else:
            self.speed_y = max(speed_y, - 1 * self.speed_y_max)
