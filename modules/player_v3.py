from PPlay.sprite import Sprite
from PPlay.window import Window
import uuid

class Player(Sprite):
    def __init__(
        self,
        acceleration=None,
        speed_x_max=None,
        speed_y_max=None,
        break_ratio=3,
        speed_shot=600,
        rate_shot=6,
        damage_shot=1,
        path_shot='imgs/shots/shot-ball-1-sm.png',
        path='imgs/ships/player/final/rotation/{}.png',
        _id=None,        
    ):
        self.path = path
        super().__init__(self.path.format(0))  # Initialize the Sprite
        self.keyboard = Window.get_keyboard()
        
        self.acceleration = acceleration
        self.speed_x_max = speed_x_max
        self.speed_y_max = speed_y_max
        self.break_ratio = break_ratio
        self.speed_shot = speed_shot
        self.rate_shot = rate_shot
        self.damage_shot = damage_shot
        self.path_shot = path_shot
        self._id = _id
        if _id is None:
            self._id_id = str(uuid.uuid4())            

        self.speed_x = 0
        self.speed_y = 0
        self.speed_x_ref = 0
        self.speed_y_ref = 0
        
        self.state_x = 'still'
        self.state_y = 'still'

    def reinitialize(self, image_path=None):
        x = self.x
        y = self.y
        if image_path is None:
            image_path = self.path.format(self.rot)
        super().__init__(image_path)
        self.set_position(x, y)
        
    def draw(self):
        super().draw()  # Call the draw method of Sprite

    def move(self, delta_x, delta_y):
        self.set_position(self.x + delta_x, self.y + delta_y)

    def accelerate(self, delta_time):
        x_dir = 0
        y_dir = 0
        rot = None
        image_path = None

        if self.keyboard.key_pressed("D"):
            x_dir += 1
            rot = 90
            # image_path = 'imgs/ships/player/final/rotation/90.png'
                
        if self.keyboard.key_pressed("A"):
            x_dir += -1
            rot = 270
            # image_path = 'imgs/ships/player/final/rotation/270.png'

        if self.keyboard.key_pressed("S"):
            y_dir += 1
            rot = 180
            # image_path = 'imgs/ships/player/final/rotation/180.png'

        if self.keyboard.key_pressed("W"):
            y_dir += -1
            rot = 0
            # image_path = 'imgs/ships/player/final/rotation/0.png'

        if all([self.keyboard.key_pressed(key) for key in ("A", "W")]):
            rot = 315
            # image_path = 'imgs/ships/player/final/rotation/315.png'

        if all([self.keyboard.key_pressed(key) for key in ("A", "S")]):
            rot = 225
            # image_path = 'imgs/ships/player/final/rotation/225.png'
        
        if all([self.keyboard.key_pressed(key) for key in ("D", "W")]):
            rot = 45
            # image_path = 'imgs/ships/player/final/rotation/45.png'
        
        if all([self.keyboard.key_pressed(key) for key in ("D", "S")]):
            rot = 135
            # image_path = 'imgs/ships/player/final/rotation/135.png'

        self.rot = rot
        if rot is not None:
            image_path = self.path.format(rot)

        # Rotate player with new angle
        if image_path is not None:
            self.reinitialize(image_path)
        #     x = self.x
        #     y = self.y
        #     super().__init__(image_path)
        #     self.set_position(x, y)

        # Update movement state
        # Break is stronger than acceleration
        acc_x = self.acceleration
        acc_y = self.acceleration

        # If movement is in both directions, adjust so the resulting  speed sum vector is equal to 1
        if not x_dir * y_dir == 0:
            acc_x = acc_x * (1 / 2 ** 0.5)
            acc_y = acc_y * (1 / 2 ** 0.5)

        if x_dir * self.speed_x > 0:
            self.state_x = 'accelerate'
        elif x_dir * self.speed_x == 0:
            self.state_x = 'still'
        else:
            self.state_x = 'break'
            acc_x *= self.break_ratio
            
        if y_dir * self.speed_y > 0:
            self.state_y = 'accelerate'
        elif y_dir * self.speed_y == 0:
            self.state_y = 'still'
        else:
            self.state_y = 'break'
            acc_y *= self.break_ratio

        # Update player speed
        speed_x = self.speed_x + x_dir * acc_x * delta_time
        speed_y = self.speed_y + y_dir * acc_y * delta_time

        if self.speed_x_max is not None:
            if speed_x >= 0:
                self.speed_x = min(speed_x, self.speed_x_max)
            else:
                self.speed_x = max(speed_x, -self.speed_x_max)

        if self.speed_y_max is not None:
            if speed_y >= 0:
                self.speed_y = min(speed_y, self.speed_y_max)
            else:
                self.speed_y = max(speed_y, -self.speed_y_max)