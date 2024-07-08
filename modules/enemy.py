import time
from PPlay.sprite import Sprite
import uuid

class Enemy(Sprite):
    def __init__(
        self,
        image_path='imgs/ships/enemy-2-60x58.png',
        speed=300, # pixels per second
        speed_shot=600, # pixels per second
        rate_shot=1, # seconds
        damage_shot=1,
        path_shot='imgs/shots/shot-ball-1-sm.png',
        positioned_y=300, # pixels 
        wait_after_positioned=2.5, # seconds
        positioned_time=None, # seconds
        life=5,
        state='positioning',
        _id=None,
    ):
        super().__init__(image_path)
        
        self.speed = speed
        self.speed_shot = speed_shot
        self.rate_shot = rate_shot
        self.damage_shot = damage_shot
        self.path_shot = path_shot
        self.positioned_y = positioned_y
        self.wait_after_positioned = wait_after_positioned
        self.positioned_time = positioned_time
        self.life = life
        self.state = state
        self._id = _id
        
        if _id is None:
            self._id = str(uuid.uuid4())            

        if positioned_time is None and state == 'positioned':
            self.positioned_time = time.time()
                
        self.speed_x = 0
        self.speed_y = 0

    def move(self, var_x, var_y):
        self.set_position(self.x + var_x, self.y + var_y)

    def auto_move(self, target, delta_time):
        if self.state == 'positioning':
            delta_y = self.speed * delta_time
            self.move(0, delta_y)
            self.speed_x = 0
            self.speed_y = delta_y / delta_time
    
            # Secondly, stop abruptly
            is_self_positioning = self.y + 0.5 * self.height < self.positioned_y
            if not is_self_positioning:
                self.state = 'positioned'
                self.positioned_time = time.time()
        
        # Thirdly, start seeking
        elif self.state == 'positioned':
            if time.time() - self.positioned_time > self.wait_after_positioned:
                self.state = 'seeking'
                self.speed = 1.3 * self.speed
            self.speed_x = 0
            self.speed_y = 0

        if self.state == 'seeking':
            dist = self.speed * delta_time

            x1, y1 = self.x - self.width / 2, self.y - self.height / 2
            x2, y2 = target.x - target.width / 2, target.y - target.height / 2

            dx = x2 - x1
            dy = y2 - y1
            norm = (dx ** 2 + dy ** 2) ** 0.5

            dx = (dx / norm) * dist
            dy = (dy / norm) * dist

            self.move(dx, dy)

            self.speed_x = dx / delta_time
            self.speed_y = dy / delta_time

        