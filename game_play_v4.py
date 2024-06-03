import time
import math

from PPlay.window import Window
from PPlay.gameimage import GameImage
from PPlay.sprite import Sprite

from modules.player_v2 import Player
from modules.shot_v2 import Shot
from modules.enemy import Enemy
from modules.game_math import calculate_horizontal_angle, calculate_horizontal_vertical_distances
from modules.image_util import get_screen_size, resize_background

enemy_ = Enemy(0, 0, None, 'imgs/ships/enemy-2-60x58.png')    

def distance(sprite1, sprite2):
    # Calculate the center points of both sprites
    center_x1 = sprite1.x + sprite1.width / 2
    center_y1 = sprite1.y + sprite1.height / 2

    center_x2 = sprite2.x + sprite2.width / 2
    center_y2 = sprite2.y + sprite2.height / 2

    # Calculate the Euclidean distance between the center points
    dist = ((center_x1 - center_x2) ** 2 + (center_y1 - center_y2) ** 2) ** 0.5

    return dist
    
class GamePlay:
    def __init__(self, difficulty, window=None, background_path="imgs/backgrounds/deep_space_gray_1280x720.png", fixed_player=False):
        self.difficulty = difficulty
        self.fixed_player = fixed_player
        self.speed_shots = 700 / self.difficulty
        self.speed_enemy = 300 / 1.3 * self.difficulty
        self.shot_min_rate = 6 / self.difficulty # shots per second
        self.player_points = 0
        self.points_base = 20
        self.last_enemy_dead_time = time.time()
        self.last_shot_time = time.time()

        if window is None:
            screen_width, screen_height = get_screen_size()
            self.window = Window(screen_width, screen_height)

        self.window = window
        self.window.set_title("Game Play")
        self.keyboard = self.window.get_keyboard()

        background_resized_path = 'imgs/backgrounds/game-play-resized.jpg'
        resize_background(background_path, background_resized_path)
        self.background = GameImage(background_resized_path)

        acceleration = 3 / self.difficulty
        speed_x_max = 500 / self.difficulty
        speed_y_max = 500 / self.difficulty
        
        self.player = Player(acceleration, speed_x_max, speed_y_max)

        x = self.window.width / 2 - self.player.sprite.width / 2
        y = self.window.height * 3 / 4 - self.player.sprite.height / 2
        self.player.sprite.set_position(x, y)
        
        self.shots = []

        n_enemies = 8
        enemy_row_width_prct = 0.7
        enemy_row_width = enemy_row_width_prct * self.window.width
        enemy_row_x_start = (1 - enemy_row_width_prct) * self.window.width / 2
        enemy_row_interval_width = (enemy_row_width - n_enemies * enemy_.sprite.width) / (n_enemies - 1)
        
        self.enemies = []
        for i in range(n_enemies):
            x = enemy_row_x_start + i * enemy_.sprite.width + i * enemy_row_interval_width
            y = (- 3) * enemy_.sprite.height
            enemy = Enemy(x, y, self.speed_enemy, 'imgs/ships/enemy-2-60x58.png')
            enemy.life = 5
            self.enemies.append(enemy)

        self.enemies_status = 'positioning'
        self.enemies_positioned_time = None
        self.enemies_seeking = False

        self.orbs = []
        for i in range(3):
            orb = Sprite('imgs/ships/orb_16.png')
            orb.x = - orb.width
            orb.y = - orb.height
            orb.speed = 600
            orb.speed_max = 600
            orb.speed_linear = 600
            orb.radius = 120
            orb.angle = 120 * i
            orb.rotation_angle = 0
            orb.tracking_distance = self.player.sprite.width * 3.5
            orb.state = 'resting'
            orb.is_on_top = False
            orb.time = time.time()
            self.orbs.append(orb)

    def run(self):
    
        while True:
            if self.keyboard.key_pressed("ESC"):
                # Wait mouse click to finish
                while self.keyboard.key_pressed("ESC"):
                    time.sleep(0.2) # busy waiting
                break

            # SIMULATE LOCKED ORBS PREVIOUS MOVEMENT
            # Move the orb with sinusoidal movement to circulate around the player along a horizontal axis                    
            for orb in self.orbs:
                player_center_x = self.player.sprite.x + self.player.sprite.width / 2
                player_center_y = self.player.sprite.y + self.player.sprite.height / 2
    
                rotating_cos = math.cos(math.radians(orb.rotation_angle))
                rotating_sin = math.sin(math.radians(orb.rotation_angle))
    
                prev_orb_x = player_center_x + orb.radius * math.cos(math.radians(orb.angle)) * rotating_cos
                prev_orb_y = player_center_y + orb.radius * math.sin(math.radians(orb.angle)) * rotating_sin

                orb.prev_x = prev_orb_x
                orb.prev_y = prev_orb_y
            
            # ---
            # MOVE AND ROTATE THE PLAYER IF MOVEMENT KEYS PRESSED

            self.player.accelerate()
            
            delta_x = self.player.speed_x  * self.window.delta_time()
            delta_y = self.player.speed_y  * self.window.delta_time()
            
            scene_delta_x = -1 * delta_x
            scene_delta_y = -1 * delta_y

            if self.fixed_player:
                for shot in self.shots:
                    shot.move(scene_delta_x, scene_delta_y)
    
                for enemy in self.enemies:
                    enemy.move(scene_delta_x, scene_delta_y)

                for orb in self.orbs:
                    orb.set_position(orb.x + scene_delta_x, orb.y + scene_delta_y)

            else:
                should_move_scene_x = (self.player.sprite.x < 0 and delta_x < 0) or (self.player.sprite.x > self.window.width - self.player.sprite.width and delta_x > 0)
                should_move_scene_y = (self.player.sprite.y < 0 and delta_y < 0) or (self.player.sprite.y > self.window.height - self.player.sprite.height and delta_y > 0)

                if should_move_scene_x:
                    for shot in self.shots:
                        shot.move(scene_delta_x, 0)
        
                    for enemy in self.enemies:
                        enemy.move(scene_delta_x, 0)

                    for orb in self.orbs:
                        orb.set_position(orb.x + scene_delta_x, orb.y)

                if should_move_scene_y:
                    for shot in self.shots:
                        shot.move(0, scene_delta_y)
        
                    for enemy in self.enemies:
                        enemy.move(0, scene_delta_y)

                    for orb in self.orbs:
                        orb.set_position(orb.x, orb.y + scene_delta_y)

                if not should_move_scene_x:
                    self.player.move(delta_x, 0)

                if not should_move_scene_y:
                    self.player.move(0, delta_y)

            # ---
            # SIMULATE LOCKED MOVEMENT FOR ORBS 
            # Move the orb with sinusoidal movement to circulate around the player along a horizontal axis
            player_center_x = self.player.sprite.x + self.player.sprite.width / 2
            player_center_y = self.player.sprite.y + self.player.sprite.height / 2

            for i, orb in enumerate(self.orbs):
                orb.angle += 180 * self.window.delta_time()
                orb.rotation_angle += 20 * self.window.delta_time()
    
                rotating_cos = math.cos(math.radians(orb.rotation_angle))
                rotating_sin = math.sin(math.radians(orb.rotation_angle))
    
                orb_x = player_center_x + orb.radius * math.cos(math.radians(orb.angle)) * rotating_cos
                orb_y = player_center_y + orb.radius * math.sin(math.radians(orb.angle)) * rotating_sin
    
                orb.curr_x = orb_x
                orb.curr_y = orb_y
                
                # ---
                # APPROXIMATE ORB SPEED
                
                # Calculate linear velocity
                dist = ((orb.curr_x - orb.prev_x) ** 2 + (orb.curr_y - orb.prev_y) ** 2) ** 0.5
                time_elapsed = self.window.delta_time()  # Time elapsed between frames
                linear_velocity = dist / time_elapsed
                
                # Set orb speed to linear velocity
                orb.speed_linear = linear_velocity

            # ---
            # MOVE ORBS WAVE
            
            for i, orb in enumerate(self.orbs):
                if orb.state == 'resting':
                    if time.time() - orb.time > 1 * (i + 1):
                        # orb.time = None
                        orb.state = 'seeking'

                if orb.state == 'seeking':
                    # Move orb towards seeking the player
                    dist = orb.speed * self.window.delta_time()
                    delta_x = self.player.sprite.x + self.player.sprite.width / 2 - orb.x - orb.width / 2
                    delta_y = self.player.sprite.y + self.player.sprite.height / 2 - orb.y - orb.height / 2
                    norm = (delta_x ** 2 + delta_y ** 2) ** 0.5
                    delta_x = (delta_x / norm) * dist
                    delta_y = (delta_y / norm) * dist

                    orb.set_position(orb.x + delta_x, orb.y + delta_y)
                    if distance(orb, self.player.sprite) < orb.tracking_distance:
                        orb.state = 'tracking'

                elif orb.state == 'tracking':
                    # Smoothly transition into the locked orbit
                    delta_x = orb.curr_x + orb.width / 2 - (orb.x + orb.width / 2)
                    delta_y = orb.curr_y + orb.height / 2 - (orb.y + orb.height / 2)
                    norm = (delta_x ** 2 + delta_y ** 2) ** 0.5

                    # Update orb speed smoothly
                    smooth_speed = orb.speed_linear + (orb.speed - orb.speed_linear) * (norm / orb.tracking_distance) ** (1/3) # Smooth factor
                    orb.speed = min(orb.speed_max, smooth_speed)
                    distance_to_move = orb.speed * time_elapsed  # Reduced speed for smooth transition

                    delta_x = (delta_x / norm) * distance_to_move
                    delta_y = (delta_y / norm) * distance_to_move

                    orb.set_position(orb.x + delta_x, orb.y + delta_y)

                    if distance(orb, self.player.sprite) > orb.tracking_distance:
                        orb.state = 'seeking'
                        orb.speed = orb.speed_max

                    delta_x = orb.curr_x + orb.width / 2 - (orb.x + orb.width / 2)
                    delta_y = orb.curr_y + orb.height / 2 - (orb.y + orb.height / 2)
                    norm = (delta_x ** 2 + delta_y ** 2) ** 0.5

                    if norm < orb.width:
                        orb.state = 'locked'
                        
                elif orb.state == 'locked':
                    # Move the orb with sinusoidal movement to circulate around the player along a horizontal axis
                    orb.x = orb.curr_x
                    orb.y = orb.curr_y
                    is_on_top_x = orb.angle % 360 < 180 # This is not working for vertical rotation
                    is_on_top_y = orb.rotation_angle % 360 < 180 # This is not working for vertical rotation
                    orb.is_on_top = is_on_top_x 
                    
            # ---
            # CREATE MULTIDIRECTION SHOTS

            if any([self.keyboard.key_pressed(key) for key in ['right', 'left', 'down', 'up']]):
                x_dir = 0
                y_dir = 0
                if self.keyboard.key_pressed("right"):
                    x_dir += + 1
                if self.keyboard.key_pressed("left"):
                    x_dir += - 1
                if self.keyboard.key_pressed("down"):
                    y_dir += + 1
                if self.keyboard.key_pressed("up"):
                    y_dir += - 1

                time_diff = time.time() - self.last_shot_time
                if time_diff > 1 / self.shot_min_rate:
                    self.last_shot_time = time.time()
                    
                    x = self.player.sprite.x + self.player.sprite.width / 2
                    y = self.player.sprite.y + self.player.sprite.width / 2
                     
                    shot = Shot(x_dir, y_dir, self.speed_shots, 'imgs/shots/shot-ball-1-sm.png')
                    shot.sprite.set_position(x, y)
                    self.shots.append(shot)

            # ---
            # MOVE MULTIDIRECTION SHOTS

            for shot in self.shots:
                delta_time = self.window.delta_time()
                shot.auto_move(delta_time)
                
            # ---
            # REMOVE MULTIDIRECTION SHOTS IF OUTSIDE WINDOW

            remove_shots = []
            for shot in self.shots:
                if shot.sprite.y <= - shot.sprite.height or shot.sprite.y >= self.window.height or shot.sprite.x <= - shot.sprite.width or shot.sprite.x >= self.window.width:
                    remove_shots.append(shot)
    
            # ---
            # REMOVE SHOT

            for shot in remove_shots:
                del self.shots[self.shots.index(shot)]
        
            # ---
            # MOVE ENEMY WAVE

            if self.enemies:
                
                # First, move then vertically while above 30% of the window height
                if self.enemies_status == 'positioning':
                    for enemy in self.enemies:
                        delta_y = enemy.speed * self.window.delta_time()
                        enemy.move(0, delta_y)
                

                # Secondly, stop abruptly
                are_enemies_positioning = self.enemies[0].sprite.y + 0.5 * self.enemies[0].sprite.height < self.window.height * 0.15
                if not are_enemies_positioning and self.enemies_status == 'positioning':
                    self.enemies_status = 'positioned'
                    self.enemies_positioned_time = time.time()
                    
                # Thirdly, start seeking
                wait_after_positioned = 2.5
                if self.enemies_status == 'positioned':
                    if time.time() - self.enemies_positioned_time > wait_after_positioned:
                        self.enemies_status = 'seeking'
                        self.enemies_positioned_time = None
        
                        for enemy in self.enemies:
                            enemy.speed = 1.3 * enemy.speed

                if self.enemies_status == 'seeking':
                    for enemy in self.enemies:
                        dist = enemy.speed * self.window.delta_time()
                        x1, y1 = enemy.sprite.x, enemy.sprite.y
                        x2, y2 = self.player.sprite.x, self.player.sprite.y
                        
                        angle_rad = calculate_horizontal_angle(x1, y1, x2, y2)
                        delta_x, delta_y = calculate_horizontal_vertical_distances(dist, angle_rad)
                                
                        enemy.move(delta_x, delta_y)

            # ---
            # HANDLE SHOT/ENEMY COLISSION
            
            if self.enemies:
                # ---
                # GET THE COORDINATES OF THE "BOX" ENCLOSING THE GRID OF ENEMIES
        
                enemy_x_min = self.window.width
                enemy_x_max = 0
                enemy_y_min = self.window.height
                enemy_y_max = 0
                for enemy in self.enemies:
                    if enemy.sprite.x < enemy_x_min:
                        enemy_x_min = enemy.sprite.x
                    if enemy.sprite.x + enemy.sprite.width > enemy_x_max:
                        enemy_x_max = enemy.sprite.x + enemy.sprite.width
                    if enemy.sprite.y < enemy_y_min:
                        enemy_y_min = enemy.sprite.y
                    if enemy.sprite.y + enemy.sprite.height > enemy_y_max:
                        enemy_y_max = enemy.sprite.y + enemy.sprite.height
                
                # ---
                # FILTER SHOTS INSIDE THE "BOX" OF ENEMIES
                
                # Filter shots inside the "box" of enemies (OPTIMIZATION # 1)
                shots_in_enemy_box = []
                for shot in self.shots:
                    if shot.sprite.x + shot.sprite.width > enemy_x_min and shot.sprite.x < enemy_x_max:
                        if shot.sprite.y + shot.sprite.height > enemy_y_min and shot.sprite.y < enemy_y_max:
                            shots_in_enemy_box.append(shot)
        
                # ---
                # TEST THE COLISION OF EACH SHOT AGAINST EACH ENEMY (ONLY FOR SHOTS INSIDE THE ENEMY "BOX")
        
                # Create sets of shots and enemies collided
                remove_shots = set()
                remove_enemies = set()
                # for shot in shots_in_enemy_box: # ONLY ITERATE TRHOUGH SHOTS INSIDE "BOX" OF ENEMIES, FROM TOP TO BOTTOM (OPTIMIZATION # 2)
                for shot in self.shots: # ONLY ITERATE TRHOUGH SHOTS INSIDE "BOX" OF ENEMIES, FROM TOP TO BOTTOM (OPTIMIZATION # 2)
                    for enemy in self.enemies: # ITERATE ENEMIES, FROM BOTTOM TO TOP (OPTIMIZATION # 3)
                        if shot.sprite.collided(enemy.sprite):
                            enemy.life -= 1
                            remove_shots.add(shot)
                            if enemy.life == 0:
                                remove_enemies.add(enemy)                
            
                # ---
                # REMOVE SHOTS AND ENEMIES COLLIDED 
                
                # Remove shots intersecting enemies
                for shot in remove_shots:
                    del self.shots[self.shots.index(shot)]
        
                # Remove enemies intersecting shots
                for enemy in remove_enemies:
                    del self.enemies[self.enemies.index(enemy)]
        
                # ---
                # UPDATE PLAYER POINTS FOR EACH DEAD ENEMIES (CUSTOM)
        
                if len(remove_enemies):
                    new_enemy_dead_time = time.time()
                    time_between_kills = new_enemy_dead_time - self.last_enemy_dead_time
                    self.last_enemy_dead_time = new_enemy_dead_time
         
                for enemy in remove_enemies:
                    delta_points = self.points_base
                    delta_points = delta_points / time_between_kills # REWARD MORE POINTS IF TIME BETWEEN KILLS DECREASES 
                    delta_points = delta_points / self.difficulty # REWARD MORE POINTS IF DIFFICULTY IS LOWER
        
                    delta_points = int(delta_points)
                    delta_points = max(1, delta_points) # MINIMUM NUMBER OF POINTS IS 1
                    
                    self.player_points += delta_points

            # ---
            # DRAW ELEMENTS
            
            self.background.draw()

            for i, orb in enumerate(self.orbs):
                self.window.draw_text(f'ORB-Vel-{i + 1}: {round(orb.speed_linear, 1)}', 20, self.window.height - 120 - i * 40, size=20, color=(255, 255, 255), font_name="arial")

            self.window.draw_text(f'Vel-X: {self.player.speed_x}', 20, self.window.height - 80, size=20, color=(255, 255, 255), font_name="arial")
            self.window.draw_text(f'Vel-Y: {self.player.speed_y}', 20, self.window.height - 40, size=20, color=(255, 255, 255), font_name="arial")

            for shot in self.shots:
                shot.draw()

            for enemy in self.enemies:
                enemy.draw()

            for orb in self.orbs:
                if not orb.is_on_top:
                    orb.draw()
    
            self.player.draw()
    
            for orb in self.orbs:
                if orb.is_on_top:
                    orb.draw()
                    
            self.window.update()

if __name__ == '__main__':
    game = GamePlay(difficulty=1, window=None)
    game.run()
