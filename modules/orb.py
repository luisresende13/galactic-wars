import math
import time
from PPlay.sprite import Sprite

def distance(sprite1, sprite2):
    # Calculate the center points of both sprites
    center_x1 = sprite1.x + sprite1.width / 2
    center_y1 = sprite1.y + sprite1.height / 2

    center_x2 = sprite2.x + sprite2.width / 2
    center_y2 = sprite2.y + sprite2.height / 2

    # Calculate the Euclidean distance between the center points
    dist = ((center_x1 - center_x2) ** 2 + (center_y1 - center_y2) ** 2) ** 0.5

    return dist

class Orb(Sprite):
    def __init__(
        self,
        image_path='imgs/ships/orb_16.png',
        speed=600,
        speed_max=600,
        radius=120,
        angle=0,
        rotation_angle=0,
        angle_rate=180,
        rotation_angle_rate=20,
        state='resting',
        wait=0,
        track_distance=100,
        lock_distance='auto',
        smooth_power=3,
        life=3,
    ):
        super().__init__(image_path)

        self.speed = speed
        self.speed_max = speed_max
        self.radius = radius
        self.angle = angle
        self.rotation_angle = rotation_angle
        self.angle_rate = angle_rate
        self.rotation_angle_rate = rotation_angle_rate
        self.state = state
        self.wait = wait
        self.track_distance = track_distance
        self.smooth_power = smooth_power
        self.life = life
        self.lock_distance = lock_distance

        if self.lock_distance == 'auto':
            self.lock_distance = self.width
            
        self.time = time.time()
        self.speed_linear = None
        self.is_on_top = False
        self.prev_x = self.x
        self.prev_y = self.y


    def move(self, delta_x, delta_y):
        self.set_position(self.x + delta_x, self.y + delta_y)

    # ---
    # SIMULATE LOCKED ORBS PREVIOUS MOVEMENT

    def update_previous_position(self, target):
        target_center_x = target.x + target.width / 2
        target_center_y = target.y + target.height / 2

        rotating_cos = math.cos(math.radians(self.rotation_angle))
        rotating_sin = math.sin(math.radians(self.rotation_angle))

        prev_orb_x = target_center_x + self.radius * math.cos(math.radians(self.angle)) * rotating_cos
        prev_orb_y = target_center_y + self.radius * math.sin(math.radians(self.angle)) * rotating_sin

        self.prev_x = prev_orb_x
        self.prev_y = prev_orb_y

    # ---
    # MOVE ORBS
    
    def update(self, target, delta_time):

        target_center_x = target.x + target.width / 2
        target_center_y = target.y + target.height / 2

        self.angle += self.angle_rate * delta_time
        self.rotation_angle += self.rotation_angle_rate * delta_time
        
        rotating_cos = math.cos(math.radians(self.rotation_angle))
        rotating_sin = math.sin(math.radians(self.rotation_angle))

        orb_x = target_center_x + self.radius * math.cos(math.radians(self.angle)) * rotating_cos
        orb_y = target_center_y + self.radius * math.sin(math.radians(self.angle)) * rotating_sin

        self.curr_x = orb_x
        self.curr_y = orb_y

        # ---
        # CHECK IF ORB IS ON TOP OR BELOW THE TARGET

        is_on_top_x = self.angle % 360 < 180 # This is not working for vertical rotation
        is_on_top_y = self.rotation_angle % 360 < 180 # This is not working for vertical rotation
        self.is_on_top = is_on_top_x

        # ---
        # APPROXIMATE THE ORB'S SPEED
        
        # Calculate linear velocity
        dist = ((self.curr_x - self.prev_x) ** 2 + (self.curr_y - self.prev_y) ** 2) ** 0.5
        linear_velocity = dist / delta_time
        
        # Set orb speed to linear velocity
        self.speed_linear = linear_velocity

        # Update previous x and y
        self.prev_x = self.curr_x
        self.prev_y = self.curr_y

        # ---
        # MOVE THE ORBS
        
        if self.state == 'resting':
            if time.time() - self.time > self.wait:
                self.state = 'seeking'
    
        if self.state == 'seeking':
            # Move orb towards seeking the target
            dist = self.speed * delta_time
            delta_x = target.x + target.width / 2 - self.x - self.width / 2
            delta_y = target.y + target.height / 2 - self.y - self.height / 2
            norm = (delta_x ** 2 + delta_y ** 2) ** 0.5
            delta_x = (delta_x / norm) * dist
            delta_y = (delta_y / norm) * dist
    
            self.move(delta_x, delta_y)
            if distance(self, target) < self.track_distance:
                self.state = 'tracking'

        elif self.state == 'tracking':
            # Get distance from current locked position
            delta_x = self.curr_x + self.width / 2 - (self.x + self.width / 2)
            delta_y = self.curr_y + self.height / 2 - (self.y + self.height / 2)
            norm = (delta_x ** 2 + delta_y ** 2) ** 0.5
    
            # Smooth transition into orbit
            smooth_speed = self.speed_linear + (self.speed - self.speed_linear) * (norm / self.track_distance) ** (1 / self.smooth_power) # Smooth power factor
            self.speed = min(self.speed_max, smooth_speed)

            distance_to_move = self.speed * delta_time
            delta_x = (delta_x / norm) * distance_to_move
            delta_y = (delta_y / norm) * distance_to_move
    
            self.move(delta_x, delta_y)

            if distance(self, target) > self.track_distance:
                self.state = 'seeking'
                self.speed = self.speed_max
    
            delta_x = self.curr_x + self.width / 2 - (self.x + self.width / 2)
            delta_y = self.curr_y + self.height / 2 - (self.y + self.height / 2)
            norm = (delta_x ** 2 + delta_y ** 2) ** 0.5
    
            if norm < self.lock_distance:
                self.state = 'locked'
                
        elif self.state == 'locked':
            # Move the orb with sinusoidal movements to circulate around the target
            self.x = self.curr_x
            self.y = self.curr_y

