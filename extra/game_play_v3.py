import time

from PPlay.window import Window
from PPlay.gameimage import GameImage

from modules.player_v2 import Player
from modules.shot_v2 import Shot
from modules.enemy import Enemy
from modules.game_math import calculate_horizontal_angle, calculate_horizontal_vertical_distances
from modules.image_util import get_screen_size, resize_background

enemy_ = Enemy(0, 0, None, 'imgs/ships/enemy-2-60x58.png')    

class GamePlay:
    def __init__(self, difficulty, window=None, background_path="imgs/backgrounds/deep_space_gray_1280x720.png", fixed_player=False):
        self.difficulty = difficulty
        self.fixed_player = fixed_player
        self.speed_shots = 700 / self.difficulty
        self.speed_enemy = 200 / 1.3 * self.difficulty
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
        speed_x_max = 450 / self.difficulty
        speed_y_max = 450 / self.difficulty
        
        self.player = Player(acceleration, speed_x_max, speed_y_max)

        x = self.window.width / 2 - self.player.sprite.width / 2
        y = self.window.height * 3 / 4 - self.player.sprite.height / 2
        self.player.sprite.set_position(x, y)
        
        self.shots = []
        self.enemies = []

        n_enemies = 8
        
        enemy_row_width_prct = 0.7
        enemy_row_width = enemy_row_width_prct * self.window.width
        enemy_row_x_start = (1 - enemy_row_width_prct) * self.window.width / 2

        enemy_row_interval_width = (enemy_row_width - n_enemies * enemy_.sprite.width) / (n_enemies - 1)
        
        for i in range(n_enemies):
            x = enemy_row_x_start + i * enemy_.sprite.width + i * enemy_row_interval_width
            y = (- 3) * enemy_.sprite.height
            enemy = Enemy(x, y, self.speed_enemy, 'imgs/ships/enemy-2-60x58.png')
            enemy.life = 5
            self.enemies.append(enemy)

        self.enemies_status = 'positioning'
        self.enemies_positioned_time = None
        self.enemies_seeking = False
    
    def run(self):
    
        while True:
            if self.keyboard.key_pressed("ESC"):
                # Wait mouse click to finish
                while self.keyboard.key_pressed("ESC"):
                    time.sleep(0.2) # busy waiting
                break

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
            
            else:
                should_move_scene_x = (self.player.sprite.x < 0 and delta_x < 0) or (self.player.sprite.x > self.window.width - self.player.sprite.width and delta_x > 0)
                should_move_scene_y = (self.player.sprite.y < 0 and delta_y < 0) or (self.player.sprite.y > self.window.height - self.player.sprite.height and delta_y > 0)

                if should_move_scene_x:
                    for shot in self.shots:
                        shot.move(scene_delta_x, 0)
        
                    for enemy in self.enemies:
                        enemy.move(scene_delta_x, 0)

                if should_move_scene_y:
                    for shot in self.shots:
                        shot.move(0, scene_delta_y)
        
                    for enemy in self.enemies:
                        enemy.move(0, scene_delta_y)

                if not should_move_scene_x:
                    self.player.move(delta_x, 0)

                if not should_move_scene_y:
                    self.player.move(0, delta_y)
            
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
                        distance = enemy.speed * self.window.delta_time()
                        x1, y1 = enemy.sprite.x, enemy.sprite.y
                        x2, y2 = self.player.sprite.x, self.player.sprite.y
                        
                        angle_rad = calculate_horizontal_angle(x1, y1, x2, y2)
                        delta_x, delta_y = calculate_horizontal_vertical_distances(distance, angle_rad)
                                
                        enemy.move(delta_x, delta_y)

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
            # Draw elements
            
            self.background.draw()

            self.window.draw_text(f'Vel-X: {self.player.speed_x}', 20, self.window.height - 80, size=20, color=(255, 255, 255), font_name="arial")
            self.window.draw_text(f'Vel-Y: {self.player.speed_y}', 20, self.window.height - 40, size=20, color=(255, 255, 255), font_name="arial")

            for shot in self.shots:
                shot.draw()

            for enemy in self.enemies:
                enemy.draw()
                
            self.player.draw()
            self.window.update()

if __name__ == '__main__':
    game = GamePlay(difficulty=1, window=None)
    game.run()