import time
from PPlay.sprite import Sprite

class Enemy(Sprite):
    def __init__(
        self,
        image_path='imgs/ships/enemy-2-60x58.png',
        speed=300,
        positioned_y=300,
        wait_after_positioned=2.5,
        positioned_time=None,
        life=5
    ):
        super().__init__(image_path)
        
        self.speed = speed
        self.positioned_y = positioned_y
        self.wait_after_positioned = wait_after_positioned
        self.positioned_time = positioned_time
        self.life = life

        self.status = 'positioning'

    def move(self, var_x, var_y):
        self.set_position(self.x + var_x, self.y + var_y)

    def auto_move(self, target, delta_time):
        if self.status == 'positioning':
            delta_y = self.speed * delta_time
            self.move(0, delta_y)
    
            # Secondly, stop abruptly
            is_self_positioning = self.y + 0.5 * self.height < self.positioned_y
            if not is_self_positioning:
                self.status = 'positioned'
                self.positioned_time = time.time()
        
        # Thirdly, start seeking
        elif self.status == 'positioned':
            if time.time() - self.positioned_time > self.wait_after_positioned:
                self.status = 'seeking'
                self.speed = 1.3 * self.speed

        if self.status == 'seeking':
            dist = self.speed * delta_time

            x1, y1 = self.x - self.width / 2, self.y - self.height / 2
            x2, y2 = target.x - target.width / 2, target.y - target.height / 2

            dx = x2 - x1
            dy = y2 - y1
            norm = (dx ** 2 + dy ** 2) ** 0.5

            dx = (dx / norm) * dist
            dy = (dy / norm) * dist

            self.move(dx, dy)

        