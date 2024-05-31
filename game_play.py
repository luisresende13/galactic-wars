import time
import math
from PPlay.window import Window
from PPlay.gameimage import GameImage

from modules.player import Player
from modules.shot import Shot
from modules.enemy import Enemy
from modules.game_math import calculate_horizontal_angle, calculate_horizontal_vertical_distances
from modules.image_util import get_screen_size, resize_background

enemy_ = Enemy(0, 0, None, 'imgs/ships/enemy-2-60x58.png')

class GamePlay:
    def __init__(self, difficulty, window=None, background_path="imgs/backgrounds/deep_space_gray_1280x720.png"):
        self.difficulty = difficulty
        self.speed_player = 300 / self.difficulty
        self.speed_shot = 700 / self.difficulty
        self.speed_enemy = 200 / 1.3 * self.difficulty
        self.shot_min_rate = 6 / self.difficulty # shots per second
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

        player_x = self.window.width / 2
        player_y = self.window.height * 13 / 16 # bottom of the self.window
        
        self.player = Player(player_x, player_y, 'imgs/ships/player/final/player-mask-sm.png')
    
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
            # MOVE THE PLAYER

            if any(list(map(self.keyboard.key_pressed, ['D', 'A', 'S', 'W']))):

                x_dir = 0
                y_dir = 0
                scene_x_dir = 0
                scene_y_dir = 0
    
                if self.keyboard.key_pressed("D"):
                    if self.player.sprite.x + self.player.sprite.width < self.window.width:
                        x_dir += + 1
                    else:
                        scene_x_dir += - 1
                        
                if self.keyboard.key_pressed("A"):
                    if self.player.sprite.x > 0:
                        x_dir += - 1
                    else:
                        scene_x_dir += + 1
    
                if self.keyboard.key_pressed("S"):
                    if self.player.sprite.y + self.player.sprite.height < self.window.height:
                        y_dir += + 1
                    else:
                        scene_y_dir += - 1
    
                if self.keyboard.key_pressed("W"):
                    if self.player.sprite.y > 0:
                        y_dir += - 1
                    else:
                        scene_y_dir += + 1
    
                # delta_x = x_dir * self.speed_player  * self.window.delta_time()
                # delta_y = y_dir * self.speed_player  * self.window.delta_time()
                # scene_delta_x = scene_x_dir * self.speed_player  * self.window.delta_time()
                # scene_delta_y = scene_y_dir * self.speed_player  * self.window.delta_time()
    
                # Use vectorial speed for each direction instead of the same full speed for each direction
                distance = self.speed_player * self.window.delta_time()
                angle_rad = math.atan2(y_dir, x_dir)
                delta_x, delta_y = calculate_horizontal_vertical_distances(distance, angle_rad)
                if y_dir == x_dir == 0:
                    delta_x = delta_y = 0
    
                distance = self.speed_player * self.window.delta_time()
                angle_rad = math.atan2(scene_y_dir, scene_x_dir)
                scene_delta_x, scene_delta_y = calculate_horizontal_vertical_distances(distance, angle_rad)
                if scene_x_dir == scene_y_dir == 0:
                    scene_delta_x = scene_delta_y = 0
    
                self.player.move(delta_x, delta_y)
    
                for shot in self.shots:
                    shot.move(scene_delta_x, scene_delta_y)
    
                for enemy in self.enemies:
                    enemy.move(scene_delta_x, scene_delta_y)

            # if self.keyboard.key_pressed("D"):
            #     x_dir += + 1
            #     if self.player.sprite.x + self.player.sprite.width < self.window.width:
            #         move_x = self.speed_player  * self.window.delta_time()
            #         self.player.move(move_x, 0)
                    
            # if self.keyboard.key_pressed("A"):
            #     x_dir += - 1
            #     if self.player.sprite.x > 0:
            #         move_x = - 1 * self.speed_player  * self.window.delta_time()
            #         self.player.move(move_x, 0)

            # if self.keyboard.key_pressed("S"):
            #     y_dir += + 1
            #     if self.player.sprite.y + self.player.sprite.height < self.window.height:
            #         move_y = self.speed_player  * self.window.delta_time()
            #         self.player.move(0, move_y)
                    
            # if self.keyboard.key_pressed("W"):
            #     y_dir += - 1
            #     if self.player.sprite.y > 0:
            #         move_y = - 1 * self.speed_player  * self.window.delta_time()
            #         self.player.move(0, move_y)

            
            # ---
            # SHOOT WITH SPACE
            
            # if self.keyboard.key_pressed("space"):
            #     time_diff = time.time() - self.last_shot_time
            #     if time_diff > 1 / self.shot_min_rate:
            #         self.last_shot_time = time.time()
                    
            #         shot_x = self.player.sprite.x + self.player.sprite.width / 2
            #         shot_y = self.player.sprite.y
                    
            #         new_shot = Shot(shot_x, shot_y, image_path='imgs/shots/shot-fire-3x-rot-final.png')
            #         self.shots.append(new_shot)
            #         print(f'NEW SHOT... N-SHOTS: {len(self.shots)}')

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
                    
                    shot_x = self.player.sprite.x + self.player.sprite.width / 2
                    shot_y = self.player.sprite.y + self.player.sprite.width / 2
                    
                    # new_shot = Shot(shot_x, shot_y, x_dir, y_dir, image_path='imgs/shots/shot-fire-3x-rot-final.png')
                    new_shot = Shot(shot_x, shot_y, x_dir, y_dir, image_path='imgs/shots/shot-ball-1-sm.png')
                    self.shots.append(new_shot)
                    print(f'N-SHOTS: {len(self.shots)}')

            # ---
            # MOVE MULTIDIRECTION SHOTS

            for shot in self.shots:
                distance = self.speed_shot * self.window.delta_time()
                angle_rad = math.atan2(shot.y_dir, shot.x_dir)
                delta_x, delta_y = calculate_horizontal_vertical_distances(distance, angle_rad)
                shot.move(delta_x, delta_y)

            # ---
            # REMOVE MULTIDIRECTION SHOTS

            remove_shot_index = []
            for i, shot in enumerate(self.shots):
                if shot.sprite.y <= - shot.sprite.height or shot.sprite.y >= self.window.height or shot.sprite.x <= - shot.sprite.width or shot.sprite.x >= self.window.width:
                    remove_shot_index.append(i)
    
            # ---
            # MOVE SINGLE DIRECTION SHOT
            
            # move_shot_y = - 1 * self.speed_shot * self.window.delta_time()
            # for shot in self.shots:
            #     shot.move(0, move_shot_y)
    
            # ---
            # REMOVE SINGLE DIRECTION SHOT

            # remove_shot_index = []
            # for i, shot in enumerate(self.shots):
            #     if shot.sprite.y <= 0:
            #         remove_shot_index.append(i)
    
            for i in remove_shot_index:
                del self.shots[i]
                print(f'N-SHOTS: {len(self.shots)}')

            # ---
            # MOVE ENEMY WAZE

            if self.enemies:
                
                # First, move then vertically while above 30% of the window height
                if self.enemies_status == 'positioning':
                    for enemy in self.enemies:
                        delta_y = enemy.speed * self.window.delta_time()
                        enemy.move(0, delta_y)
                

                # Secondly, stop abruptly
                are_enemies_positioning = self.enemies[0].sprite.y + 0.5 * self.enemies[0].sprite.height < 0.3 * self.window.height
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
                    
            
            # ---
            
            # Draw elements
            
            self.background.draw()
            
            for shot in self.shots:
                shot.draw()

            for enemy in self.enemies:
                enemy.draw()
                
            self.player.draw()
            self.window.update()

if __name__ == '__main__':
    game = GamePlay(difficulty=1, window=None)
    game.run()