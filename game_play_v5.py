
# BUGS:

# Impedir tiro de monstros fora da tela ou a partir de uma certa distancia


# UPDATES:
# - Mostrar vida do player
# - refazer logica de ordas em fases (como?)
# - primeira fase inimigos sem tiro

# TO-DO:
# 1. Add radar map
# 1. Add life bar to player, enemies and orbs
# 1. Dar zoom no sprite de background e/ou aumentar resolução (para evitar ver as bordas da imagem)
# 1. Sprites de fundos oceânico, terrestre (e espaciais?)
# 1. Sprites de inimígos diferentes + código
# 1. Sprites de tiros diferentes + código
# 1. Sprite nave-mãe + código
# 1. Sprites explosões diferentes + código
# 1. Baixar áudio de fundo + código
# 1. Baixar áudio de explosões + código
# 1. Ao final, ajustar parâmetros, tamanhos e sprites e fases

# EXTRA:
# 1. Sprites de obstáculos? Satélites e naves destruidos + código (sprite de obstaculos possui rotação aleatória)
# 1. Sprite de orbs
# 1. Sprite de brilho por trás "orbs" quando se travam ao player + código
# 1. Player perde quando 3 orbs se travam por X segundos
# 1. Efeito abdução por orbs
# 1. Mudar dinamicamente tamanho de explosão da abdução por orbs 
# 1. Poderes especiais (aumentar ataque ou defesa)
# 1. Tela de regras
# 1. Inimigos aleatórios vêm de posições aleatórias em lados aleatórios em tempos aleatorios


import os
import time
import json
import math
import numpy as np

from PPlay.window import Window
from PPlay.gameimage import GameImage
from PPlay.sprite import Sprite

from modules.player_v3 import Player
from modules.shot_v2 import Shot
from modules.enemy import Enemy
from modules.orb import Orb
from modules.animation import Animation
from modules.game_math import calculate_horizontal_angle, calculate_horizontal_vertical_distances
from modules.image_util import get_screen_size, resize_background

enemy_ = Enemy('imgs/ships/enemy-2-60x58.png')

difficulty_names = {
    1: 'Easy',
    2: 'Medium',
    3: 'hard',
}

import pygame
def get_text_width(text, size, font_name="Arial", bold=False, italic=False):
    pygame.init()
    font = pygame.font.SysFont(font_name, size, bold, italic)
    font_surface = font.render(text, True, (0, 0, 0))
    return font_surface.get_width()


class GamePlay:
    def __init__(self, difficulty, window=None, background_path="imgs/backgrounds/deep_space_gray_1280x720.png", fixed_player=False, player_x_lim=0.40, player_y_lim=0.45, shoot_key='mouse'):
        self.window = window
        self.window.set_title("Game Play")
        self.keyboard = self.window.get_keyboard()
        self.mouse = self.window.get_mouse()
        
        self.difficulty = difficulty
        self.fixed_player = fixed_player
        self.player_points = 0
        self.points_base = 20
        self.last_enemy_dead_time = time.time()
        self.last_shot_time = time.time()
        self.player_x_lim = player_x_lim
        self.player_y_lim = player_y_lim
        self.shoot_key = shoot_key
        
        self.player = Player(
            acceleration=None,
            speed_x_max=None,
            speed_y_max=None,
            break_ratio=3,
            speed_shot=600,
            rate_shot=6,
            damage_shot=1,
            path_shot='imgs/shots/shot-ball-1-sm.png',
            path='imgs/ships/player/final/rotation/{}.png',
        )
        self.player.life = 5
        x = self.window.width / 2 - self.player.width / 2
        y = self.window.height * 3 / 4 - self.player.height / 2
        if fixed_player:
            x = self.window.width / 2 - self.player.width / 2
            y = self.window.height / 2 - self.player.height / 2
        self.player.set_position(x, y)

        self.increase_difficulty(delta=0)
        
        if window is None:
            screen_width, screen_height = get_screen_size()
            self.window = Window(screen_width, screen_height)

        background_resized_path = 'imgs/backgrounds/game-play-resized.jpg'
        resize_background(background_path, background_resized_path)
        self.background = GameImage(background_resized_path)

        # Start phase counter
        self.phase = 0
        
        # Shots
        self.shots = []

        # Enemies
        self.enemies = []
        self.enemy_wave_counter = 0
        self.created_enemy_wave = False
        # self.create_enemy_cloud(100)
        # self.create_enemy_row(n_enemies=8, enemy_row_width_prct=0.7, enemy_row_positioned_y_prct=0.15)        

        # Orbs
        self.orbs = []
        self.orbs_wave = 0
        # self.create_orbs(n=3, wait_between=2)

        # Explosions
        self.explosions = []

        # End game flag
        self.game_ended = False

        # Phase configuration
        self.phases = json.load(open('phases.json', 'r'))

    # # Update difficulty
    def increase_difficulty(self, delta=1):
        self.difficulty += delta
        self.player.acceleration = 300 - 1.0 * (self.difficulty - 1) # good value: 5.0, 10.0 ...
        self.player.speed_x_max = 500 - 100 * (self.difficulty - 1) # good value: 500.0, 750.0 ...
        self.player.speed_y_max = 500 - 100 * (self.difficulty - 1) # good value: 500.0, 750.0 ...
        self.player.speed_shot = 600 - 150 * (self.difficulty - 1)
        self.player.rate_shot = 6 - 1 * (self.difficulty - 1) # shots per second

    # def create_enemy_cloud(self, n_enemies=8, x_lim=(-10000, 10000), y_lim=(-10000, 10000)):
        # xi = np.random.uniform(x_lim[0], x_lim[1], n_enemies)
        # yi = np.random.uniform(y_lim[0], y_lim[1], n_enemies)

    def create_enemy_cloud(
        self,
        origin,
        n_enemies=30,
        min_dist=500,
        max_dist=5000,
        config=dict(
            image_path='imgs/ships/enemy-2-42x41.png',
            life=3,
            speed=200,
            speed_shot=600,
            rate_shot=1,
            damage_shot=1,
            path_shot='imgs/shots/shot-ball-1-sm.png',
            state='seeking',
            positioned_y=300,
            wait_after_positioned=2.5,
            positioned_time=None,
        )
    ):
        x, y = origin

        # Generate random distances and angles
        distances = np.random.uniform(min_dist, max_dist, n_enemies)
        angles = np.random.uniform(0, 2 * np.pi, n_enemies)
        
        # Convert polar coordinates to Cartesian coordinates
        xi = x + distances * np.cos(angles)
        yi = y + distances * np.sin(angles)

        for i, (x, y) in enumerate(zip(xi, yi)):
            enemy = Enemy(**config)
            enemy.set_position(x, y)
            enemy.last_shot_time = time.time()

            self.enemies.append(enemy)

    def create_enemy_row(self, n_enemies=8, speed=200, enemy_row_width_prct=0.7, enemy_row_positioned_y_prct=0.15):
        enemy_row_width = enemy_row_width_prct * self.window.width
        enemy_row_x_start = (1 - enemy_row_width_prct) * self.window.width / 2
        enemy_row_interval_width = (enemy_row_width - n_enemies * enemy_.width) / (n_enemies - 1)
        
        for i in range(n_enemies):
            enemy = Enemy(
                image_path='imgs/ships/enemy-2-42x41.png',
                speed=speed,
                positioned_y=self.window.height * enemy_row_positioned_y_prct,
                # wait_after_positioned=2.5,
                # positioned_time=None,
                life=3,
                # state='positioning',
            )

            x = enemy_row_x_start + i * enemy.width + i * enemy_row_interval_width
            y = (- 3) * enemy.height
            enemy.set_position(x, y)

            enemy.last_shot_time = time.time()

            self.enemies.append(enemy)

    def create_orbs(
        self,
        n=3,
        wait=0,
        wait_between=2,
        config=dict(
            image_path='imgs/ships/orb-1-24px.png',
            image_path_locked='imgs/ships/orb-1-24px.png',
            speed=600,
            life=3,
            state='resting',
        )
    ):
        for i in range(n):
            angle = int(360 / n) * i
            track_distance = self.player.width * 3.5
            wait = wait + wait_between * (i + 1)

            config['angle'] = angle
            config['track_distance'] = track_distance
            config['wait'] = wait

            orb = Orb(**config)
            x = - orb.width
            y = - orb.height
            orb.set_position(x, y)

            self.orbs.append(orb)

    def show_you_lose(self):
        you_lose_image_path = 'imgs/messages/end-1.jpg'
        you_lose = Sprite(you_lose_image_path)
        you_lose.set_position(self.window.width / 2 - you_lose.width / 2, self.window.height / 2 - you_lose.height / 2)

        self.background.draw()
        you_lose.draw()
        self.window.update()

        # WAIT ESC KEY DOWN
        while not self.keyboard.key_pressed("ESC"):
            time.sleep(0.2) # busy waiting

        # WAIT ESC KEY UP
        while self.keyboard.key_pressed("ESC"):
            time.sleep(0.2) # busy waiting

    def run(self):
        while True:
            # ---
            # DRAW ELEMENTS
            
            self.background.draw()
            
            for i, orb in enumerate(self.orbs):
                if orb.speed_linear is not None:
                    self.window.draw_text(f'ORB-Vel-{i + 1}: {round(orb.speed_linear, 1)}', 20, self.window.height - 120 - i * 40, size=20, color=(255, 255, 255), font_name="arial")

            self.window.draw_text(f'Vel-X: {self.player.speed_x}', 20, self.window.height - 80, size=20, color=(255, 255, 255), font_name="arial")
            self.window.draw_text(f'Vel-Y: {self.player.speed_y}', 20, self.window.height - 40, size=20, color=(255, 255, 255), font_name="arial")

            text_font = "arialblack"
            text_color = (255, 255, 0)  # Yellow
            self.window.draw_text(f'POINTS: {self.player_points}', 20, 10, size=40, color=text_color, font_name=text_font)

            phase = self.phases[self.phase - 1]
            waves = phase['waves']
            wave = waves[self.enemy_wave_counter - 1]
            n_enemies = sum([enemy["n_enemies"] for enemy in wave["enemies"]])
            kills = n_enemies - len(self.enemies)
            self.window.draw_text(f'LIFE: {self.player.life}', self.window.width - 165, 20, size=20, color=text_color, font_name=text_font)
            self.window.draw_text(f'KILLS: {kills} / {n_enemies}', self.window.width - 165, 55, size=20, color=text_color, font_name=text_font)
            self.window.draw_text(f'WAVE: {self.enemy_wave_counter} / {len(waves)}', self.window.width - 165, 90, size=20, color=text_color, font_name=text_font)
            self.window.draw_text(f'LEVEL: {self.phase} / {len(self.phases)}', self.window.width - 165, 125, size=20, color=text_color, font_name=text_font)

            self.window.draw_text(f'DIFFICULTY: {difficulty_names[self.difficulty]}', self.window.width - 225, self.window.height - 40, size=20, color=text_color, font_name=text_font)

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

            # Draw the animation
            remove_explosions = []
            for explosion in self.explosions:
                explosion.update()
                if explosion.is_finished: 
                    remove_explosions.append(explosion)
                else:
                    # explosion.move(self.animation.sprite.x + 10, self.animation.sprite.y + 10)
                    explosion.draw()
                    
            for explosion in remove_explosions:
                index = remove_explosions.index(explosion)
                del remove_explosions[index]

            self.window.update()

            # EXIT ON ESC KEY PRESSED
            if self.keyboard.key_pressed("ESC"):
                # Wait ESC KEY
                while self.keyboard.key_pressed("ESC"):
                    time.sleep(0.2) # busy waiting
                break

            # ---
            # MOVE EXPLOSIONS AT CONSTANT SPEED
            for explosion in self.explosions:
                dx = explosion.speed_x * self.window.delta_time()
                dy = explosion.speed_y * self.window.delta_time()
                explosion.move(explosion.sprite.x + dx, explosion.sprite.y + dy)
            
            # ---
            # MOVE AND ROTATE THE PLAYER IF MOVEMENT KEYS PRESSED

            if not self.game_ended:
                self.player.accelerate(self.window.delta_time())

            if not self.created_enemy_wave: # To avoid the frame with higher time delay

                delta_x = self.player.speed_x  * self.window.delta_time()
                delta_y = self.player.speed_y  * self.window.delta_time()

                self.speed_x_ref = delta_x / self.window.delta_time()
                self.speed_y_ref = delta_y / self.window.delta_time()
                
                scene_delta_x = - 1 * delta_x
                scene_delta_y = - 1 * delta_y
                
                if self.fixed_player:

                    # Background moves slowly against player
                    self.background.x += scene_delta_x * 0.07
                    self.background.y += scene_delta_y * 0.07
                    
                    for shot in self.shots:
                        shot.move(scene_delta_x, scene_delta_y)
        
                    for enemy in self.enemies:
                        enemy.move(scene_delta_x, scene_delta_y)
    
                    for orb in self.orbs:
                        orb.set_position(orb.x + scene_delta_x, orb.y + scene_delta_y)

                    for explosion in self.explosions:
                        explosion.move(explosion.sprite.x + scene_delta_x, explosion.sprite.y + scene_delta_y)
                        
                else:
                    # x_lim = (0, self.window.width - self.player.width)
                    # x_lim = (0, self.window.height - self.player.height)
                    
                    x_lim = (self.window.width * self.player_x_lim, self.window.width - self.window.width * self.player_x_lim)
                    y_lim = (self.window.height * self.player_y_lim, self.window.height - self.window.height * self.player_y_lim)

                    should_move_scene_x = (self.player.x < x_lim[0] and delta_x < 0) or (self.player.x > x_lim[1] and delta_x > 0)
                    should_move_scene_y = (self.player.y < y_lim[0] and delta_y < 0) or (self.player.y > y_lim[1] and delta_y > 0)

                    if should_move_scene_x:
                        # Background moves slowly against player
                        self.background.x += scene_delta_x * 0.07

                        for shot in self.shots:
                            shot.move(scene_delta_x, 0)
            
                        for enemy in self.enemies:
                            enemy.move(scene_delta_x, 0)
    
                        for orb in self.orbs:
                            orb.set_position(orb.x + scene_delta_x, orb.y)

                        for explosion in self.explosions:
                            explosion.move(explosion.sprite.x + scene_delta_x, explosion.sprite.y)

    
                    if should_move_scene_y:
                        # Background moves slowly against player
                        self.background.y += scene_delta_y * 0.07
                        
                        for shot in self.shots:
                            shot.move(0, scene_delta_y)
            
                        for enemy in self.enemies:
                            enemy.move(0, scene_delta_y)
    
                        for orb in self.orbs:
                            orb.set_position(orb.x, orb.y + scene_delta_y)
    
                        for explosion in self.explosions:
                            explosion.move(explosion.sprite.x, explosion.sprite.y + scene_delta_y)

                    if not should_move_scene_x:
                        self.player.move(delta_x, 0)
    
                    if not should_move_scene_y:
                        self.player.move(0, delta_y)

            # ---
            # HANDLE ABDUCTION BY ORB

            if len(self.orbs):
                orbs_locked = [orb for orb in self.orbs if orb.is_locked == True]
                if len(orbs_locked) >= 3:
                    orbs_locked = sorted(orbs_locked, key=lambda orb: orb.time_locked)
                    orbs_locked = orbs_locked[:3]

                    if min([orb.time_locked for orb in orbs_locked]) >= 5.0:    
                        # Create a Animation instance for abduction
                        explosion_path = 'imgs/effects/explosions/0-160px'
                        sorted_paths = sorted(os.listdir(explosion_path), key=lambda path: int(path.split('.png')[0]))
                        images = [f'{explosion_path}/{path}' for path in sorted_paths if path.endswith('.png')]
                        images = images[:3]
                        
                        animation = Animation(images, duration=1.01)
                        animation.start()
        
                        x = self.player.x + self.player.width / 2 - animation.sprite.width / 2
                        y = self.player.y + self.player.height / 2 - animation.sprite.height / 2
                        animation.move(x, y)
                        
                        animation.speed_x = self.player.speed_x
                        animation.speed_y = self.player.speed_y
                        
                        self.explosions.append(animation)

                        # Remove three locked orbs
                        for orb in orbs_locked:
                            del self.orbs[self.orbs.index(orb)]
    
                        # Remove player
                        self.player.reinitialize('imgs/ships/empty.png')
                        
                        # Wait game ending (End game)
                        self.game_ended = True
                        self.game_ended_counter = 0.0
            
            # ---
            # CREATE SHOTS FROM PLAYER

            # if self.shoot_key == 'arrows': 
            if any([self.keyboard.key_pressed(key) for key in ['right', 'left', 'down', 'up']]):
                time_diff = time.time() - self.last_shot_time

                if time_diff > 1 / self.player.rate_shot:
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

                    self.last_shot_time = time.time()

                    # If movement is in both directions, adjust so the resulting  speed sum vector is equal to 1
                    if not x_dir * y_dir == 0:
                        x_dir = x_dir * (1 / 2 ** 0.5)
                        y_dir = y_dir * (1 / 2 ** 0.5)

                    # shot = Shot(x_dir, y_dir, self.player.speed_shot, self.player.damage_shot, self.player.path_shot, shooter_id='player')
                    
                    # Combine the shot direction with the player's speed
                    x_dir = x_dir * self.player.speed_shot + self.player.speed_x
                    y_dir = y_dir * self.player.speed_shot + self.player.speed_y
                    combined_speed = np.sqrt(x_dir**2 + y_dir**2)
            
                    # Normalize the new direction vectors to maintain consistent shot speed
                    x_dir /= combined_speed
                    y_dir /= combined_speed
                    shot_speed = combined_speed

                    shot = Shot(x_dir, y_dir, shot_speed, self.player.damage_shot, self.player.path_shot, shooter_id='player')
                    shot.is_from_enemy = False
                    
                    x = self.player.x + self.player.width / 2
                    y = self.player.y + self.player.width / 2
                    shot.sprite.set_position(x, y)

                    self.shots.append(shot)

            # if self.shoot_key == 'mouse':
            if self.mouse.is_button_pressed(1):
                time_diff = time.time() - self.last_shot_time
                
                if time_diff > 1 / self.player.rate_shot:
                    self.last_shot_time = time.time()
                
                    target_x, target_y = self.mouse.get_position()
                    
                    dx = target_x - self.player.x
                    dy = target_y - self.player.y
                    distance = np.sqrt(dx**2 + dy**2)
                    
                    # Normalize the direction vectors
                    x_dir = dx / distance
                    y_dir = dy / distance
                    # shot_speed = self.player.speed_shot

                    # Combine the shot direction with the player's speed
                    x_dir = x_dir * self.player.speed_shot + self.player.speed_x
                    y_dir = y_dir * self.player.speed_shot + self.player.speed_y
                    combined_speed = np.sqrt(x_dir**2 + y_dir**2)
            
                    # Normalize the new direction vectors to maintain consistent shot speed
                    x_dir /= combined_speed
                    y_dir /= combined_speed
                    shot_speed = combined_speed

                    shot = Shot(x_dir, y_dir, shot_speed, self.player.damage_shot, self.player.path_shot, shooter_id='player')
                    shot.is_from_enemy = False
                    
                    x = self.player.x + self.player.width / 2
                    y = self.player.y + self.player.width / 2
                    shot.sprite.set_position(x, y)

                    self.shots.append(shot)

            # ---
            # CREATE SHOTS FROM ENEMIES

            for enemy in self.enemies:
                t = time.time()
                time_diff = t - enemy.last_shot_time

                is_enemy_on_window = (enemy.x + enemy.width > 0 and enemy.x < self.window.width) and (enemy.y + enemy.height > 0 and enemy.y < self.window.height)
                
                if is_enemy_on_window and time_diff > 1 / enemy.rate_shot:
                    enemy.last_shot_time = time.time()

                    dx = self.player.x - enemy.x
                    dy = self.player.y - enemy.y
                    
                    distance = np.sqrt(dx**2 + dy**2)
                    
                    # Normalize the direction vectors
                    x_dir = dx / distance
                    y_dir = dy / distance                    
                    
                    shot = Shot(x_dir, y_dir, enemy.speed_shot, enemy.damage_shot, enemy.path_shot, shooter_id=enemy._id)
                    shot.is_from_enemy = True
                    
                    x = enemy.x + enemy.width / 2
                    y = enemy.y + enemy.width / 2
                    shot.sprite.set_position(x, y)

                    self.shots.append(shot)

            # ---
            # MOVE SHOTS

            for shot in self.shots:
                delta_time = self.window.delta_time()
                shot.auto_move(delta_time)
                
            # ---
            # LIST INDEX OF SHOTS TOO FAR OUTSIDE WINDOW

            remove_shots = []
            for shot in self.shots:
                x_lim_shots = (- shot.sprite.width - self.window.width * 3, self.window.width * 3)
                y_lim_shots = (- shot.sprite.height - self.window.height * 3, self.window.height * 3)
                if shot.sprite.y <= y_lim_shots[0] or shot.sprite.y >= y_lim_shots[1] or shot.sprite.x <= x_lim_shots[0] or shot.sprite.x >= x_lim_shots[1]:
                    remove_shots.append(shot)
    
            # ---
            # REMOVE SHOT

            for shot in remove_shots:
                del self.shots[self.shots.index(shot)]

            # ---
            # MOVE ORBS
            
            if not self.created_enemy_wave:
                for i, orb in enumerate(self.orbs):
                    orb.update(self.player, self.window.delta_time())

            # ---
            # MOVE ENEMIES

            if not self.created_enemy_wave:
                if self.enemies:
                    for enemy in self.enemies:
                        enemy.auto_move(self.player, self.window.delta_time())

            # ---
            # CREATE ENEMY WAVE (CHANGE PHASE LEVEL)

            self.created_enemy_wave = False
            if len(self.enemies) == 0:
                self.created_enemy_wave = True
                
                # ---
                # NEXT WAVE

                # Update enemy wave counter
                self.enemy_wave_counter += 1

                phase = self.phases[self.phase - 1]
                waves = phase['waves']
                orbs = phase['orbs']

                if self.enemy_wave_counter != 1 and not self.enemy_wave_counter == len(waves) + 1:
                    # Display message for next wave
                    text = f"WAVE {self.enemy_wave_counter} / {len(waves)}"
                    yellow = (255, 255, 0)  # Yellow
                    text_size = 70
                    font_name = "arialblack"
                    x = self.window.width / 2 - get_text_width(text, text_size, font_name) / 2
                    y = self.window.height / 2 - text_size / 2
                    self.window.draw_text(text, x, y, size=text_size, color=yellow, font_name=font_name)
                    self.window.update()

                    time.sleep(3)

                # ---
                # NEXT PHASE
                
                if self.enemy_wave_counter == 1 or self.enemy_wave_counter == len(waves) + 1:

                    # Update phase
                    self.phase += 1

                    # End game if phases are over
                    if self.phase == len(self.phases) + 1:
                        you_win_image_path = 'imgs/messages/you-win-0.jpg'
                        you_win = Sprite(you_win_image_path)
                        you_win.set_position(self.window.width / 2 - you_win.width / 2, self.window.height / 2 - you_win.height / 2)

                        self.background.draw()
                        you_win.draw()
                        self.window.update()
            
                        # WAIT ESC KEY DOWN
                        while not self.keyboard.key_pressed("ESC"):
                            time.sleep(0.2) # busy waiting

                        # WAIT ESC KEY UP
                        while self.keyboard.key_pressed("ESC"):
                            time.sleep(0.2) # busy waiting

                        return # EXIT THE GAME
                        
                    # Restart enemy wave counter for next phase
                    self.enemy_wave_counter = 1

                    # Restart obs wave counter for next phase
                    self.orbs_wave = 0

                    # Display message for next phase
                    text = f"LEVEL {self.phase}"
                    yellow = (255, 255, 0)  # Yellow
                    text_size = 70
                    font_name = "arialblack"
                    x = self.window.width / 2 - get_text_width(text, text_size, font_name) / 2
                    y = self.window.height / 2 - text_size / 2
                    self.window.draw_text(text, x, y, size=text_size, color=yellow, font_name=font_name)
                    self.window.update()

                    time.sleep(3)
                    
                    if self.phase > 1:
                        # # Update difficulty
                        self.increase_difficulty(delta=1)

                # Create enemy wave
                phase = self.phases[self.phase - 1]
                waves = phase['waves']
                wave = waves[self.enemy_wave_counter - 1]
                enemies = wave['enemies']
                for config in enemies:
                    origin = (self.player.x, self.player.y)
                    self.create_enemy_cloud(origin=origin, **config)

                    # base_n_enemies = 3
                    # base_enemy_row_width_prct = 0.3
                    # n_enemies = base_n_enemies * self.enemy_wave_counter
                    # enemy_row_width_prct = base_enemy_row_width_prct * self.enemy_wave_counter
                    # self.create_enemy_row(n_enemies=n_enemies, enemy_row_width_prct=enemy_row_width_prct, enemy_row_positioned_y_prct=0.15)

            # ---
            # CREATE ORBS

            if len(self.orbs) == 0:
                self.orbs_wave += 1
                phase = self.phases[self.phase - 1]
                orbs_waves = phase['orbs']
    
                if self.orbs_wave <= len(orbs_waves):
                    config = orbs_waves[self.orbs_wave - 1]
                    self.create_orbs(**config)

            # ---
            # HANDLE COLISION OF SHOT AND SHOT
                
            remove_shots = set()
            for shot in self.shots:
                for shot_ in self.shots:
                    if self.shots.index(shot) < self.shots.index(shot_):
                        if shot.sprite.collided(shot_.sprite):
                            remove_shots.add(shot)
                            remove_shots.add(shot_)
                            
                            # Create a Animation instance for explosion
                            explosion_path = 'imgs/effects/explosions/0-24px'
                            sorted_paths = sorted(os.listdir(explosion_path), key=lambda path: int(path.split('.png')[0]))
                            images = [f'{explosion_path}/{path}' for path in sorted_paths if path.endswith('.png')]
                            
                            animation = Animation(images, duration=3)
                            animation.start()
            
                            x = shot.sprite.x + shot.sprite.width / 2 - animation.sprite.width / 2
                            y = shot.sprite.y + shot.sprite.height / 2 - animation.sprite.height / 2
                            animation.move(x, y)
                            
                            animation.speed_x = 0
                            animation.speed_y = 0
                            # animation.speed_x = shot.speed_x
                            # animation.speed_y = shot.speed_y
                            
                            self.explosions.append(animation)

            # Remove shots
            for shot in remove_shots:
                del self.shots[self.shots.index(shot)]

            # ---
            # HANDLE COLISION OF SHOT AND PLAYER

            remove_shots = set()
            for shot in self.shots:
                if shot.is_from_enemy and shot.sprite.collided(self.player):
                    remove_shots.add(shot)
                    self.player.life -= shot.damage
                    
                    if self.player.life <= 0:
                        # End game
                        self.game_ended = True
                        self.game_ended_counter = 0.0
                        
                        # Create a Animation instance for explosion
                        explosion_path = 'imgs/effects/explosions/0-76px'
                        sorted_paths = sorted(os.listdir(explosion_path), key=lambda path: int(path.split('.png')[0]))
                        images = [f'{explosion_path}/{path}' for path in sorted_paths if path.endswith('.png')]
                        animation = Animation(images, duration=3)
                        animation.start()
                        
                        animation.speed_x = self.player.speed_x 
                        animation.speed_y = self.player.speed_y
                        
                        x = self.player.x + self.player.width / 2 - animation.sprite.width / 2
                        y = self.player.y + self.player.height / 2 - animation.sprite.height / 2
                        animation.move(x, y)

                        self.explosions.append(animation)

            if self.game_ended:
                self.game_ended_counter += self.window.delta_time()
                if self.game_ended_counter > 3:
                    self.show_you_lose()
            
                    return # EXIT THE GAME
                        
            # Remove shots
            for shot in remove_shots:
                del self.shots[self.shots.index(shot)]

            # ---
            # HANDLE COLISION OF PLAYER AND ENEMY 
            
            if self.enemies:
                
                # ---
                # GET THE COORDINATES OF THE "BOX" ENCLOSING THE GRID OF ENEMIES
        
                enemy_x_min = self.window.width
                enemy_x_max = 0
                enemy_y_min = self.window.height
                enemy_y_max = 0
                remove_enemies = set()

                for enemy in self.enemies:
                    if enemy.x < enemy_x_min:
                        enemy_x_min = enemy.x
                    if enemy.x + enemy.width > enemy_x_max:
                        enemy_x_max = enemy.x + enemy.width
                    if enemy.y < enemy_y_min:
                        enemy_y_min = enemy.y
                    if enemy.y + enemy.height > enemy_y_max:
                        enemy_y_max = enemy.y + enemy.height

                    # ---
                    # HANDLE COLISION OF PLAYER AND ENEMY (END GAME)
    
                    if self.player.collided(enemy):
                        remove_enemies.add(enemy)
            
                        # End game
                        self.game_ended = True
                        self.game_ended_counter = 0.0
                        
                        # Create a Animation instance for explosion
                        explosion_path = 'imgs/effects/explosions/0-76px'
                        sorted_paths = sorted(os.listdir(explosion_path), key=lambda path: int(path.split('.png')[0]))
                        images = [f'{explosion_path}/{path}' for path in sorted_paths if path.endswith('.png')]
                        animation = Animation(images, duration=3)
                        animation.start()
                        
                        animation.speed_x = self.player.speed_x
                        animation.speed_y = self.player.speed_y
                        
                        x = self.player.x + self.player.width / 2 - animation.sprite.width / 2
                        y = self.player.y + self.player.height / 2 - animation.sprite.height / 2
                        animation.move(x, y)

                        self.explosions.append(animation)
    
                if self.game_ended:
                    self.game_ended_counter += self.window.delta_time()
                    if self.game_ended_counter > 3:
                        self.show_you_lose()
                
                        return # EXIT THE GAME

                # ---
                # FILTER SHOTS INSIDE ENEMY BOX
    
                shots_in_enemy_box = []
                for shot in self.shots:
                    if shot.sprite.x + shot.sprite.width > enemy_x_min and shot.sprite.x < enemy_x_max:
                        if shot.sprite.y + shot.sprite.height > enemy_y_min and shot.sprite.y < enemy_y_max:
                            shots_in_enemy_box.append(shot)

                # Remove enemies
                for enemy in remove_enemies:
                    del self.enemies[self.enemies.index(enemy)]
        
            # ---
            # HANDLE COLISION OF SHOT AND ENEMY
    
            # Create sets of shots and enemies collided
            remove_shots = set()
            remove_enemies = set()
            remove_orbs = set()
            # for shot in shots_in_enemy_box: # ONLY ITERATE TRHOUGH SHOTS INSIDE "BOX" OF ENEMIES, FROM TOP TO BOTTOM (OPTIMIZATION # 2)
            for shot in self.shots: # ONLY ITERATE TRHOUGH SHOTS INSIDE "BOX" OF ENEMIES, FROM TOP TO BOTTOM (OPTIMIZATION # 2)
                # if not shot.is_from_enemy:
                for enemy in self.enemies: # ITERATE ENEMIES, FROM BOTTOM TO TOP (OPTIMIZATION # 3)
                    if not shot.shooter_id == enemy._id and shot.sprite.collided(enemy):
                        enemy.life -= shot.damage
                        remove_shots.add(shot)
                        if enemy.life <= 0:
                            # Remove enemy
                            remove_enemies.add(enemy)

                            # Create a Animation instance for explosion
                            explosion_path = 'imgs/effects/explosions/0-76px'
                            sorted_paths = sorted(os.listdir(explosion_path), key=lambda path: int(path.split('.png')[0]))
                            images = [f'{explosion_path}/{path}' for path in sorted_paths if path.endswith('.png')]
                            animation = Animation(images, duration=3)
                            animation.start()
                            x = enemy.x + enemy.width / 2 - animation.sprite.width / 2
                            y = enemy.y + enemy.height / 2 - animation.sprite.height / 2
                            animation.move(x, y)
                            animation.speed_x = enemy.speed_x
                            animation.speed_y = enemy.speed_y
                            self.explosions.append(animation)

                # ---
                # HANDLE COLISION OF SHOT AND ORBS

                for orb in self.orbs: # ITERATE ORBS
                    if shot.sprite.collided(orb):
                        orb.life -= shot.damage
                        remove_shots.add(shot)
                        if orb.life <= 0:
                            remove_orbs.add(orb)

                            # Create a Animation instance for explosion
                            explosion_path = 'imgs/effects/explosions/0-24px'
                            sorted_paths = sorted(os.listdir(explosion_path), key=lambda path: int(path.split('.png')[0]))
                            images = [f'{explosion_path}/{path}' for path in sorted_paths if path.endswith('.png')]
                            
                            animation = Animation(images, duration=3)
                            animation.start()

                            x = orb.x + orb.width / 2 - animation.sprite.width / 2
                            y = orb.y + orb.height / 2 - animation.sprite.height / 2
                            animation.move(x, y)
                            
                            animation.speed_x = orb.speed_x
                            animation.speed_y = orb.speed_y
                            
                            self.explosions.append(animation)
        
            # ---
            # REMOVE SHOTS AND ENEMIES COLLIDED 
            
            # Remove shots
            for shot in remove_shots:
                del self.shots[self.shots.index(shot)]
    
            # Remove enemies
            for enemy in remove_enemies:
                del self.enemies[self.enemies.index(enemy)]

            # Remove orbs
            for orb in remove_orbs:
                del self.orbs[self.orbs.index(orb)]

            # ---
            # UPDATE PLAYER POINTS FOR DEAD ENEMIES (CUSTOM)
    
            if len(remove_enemies):
                new_enemy_dead_time = time.time()
                time_between_kills = new_enemy_dead_time - self.last_enemy_dead_time
                self.last_enemy_dead_time = new_enemy_dead_time
     
            for enemy in remove_enemies:
                dist = ((self.player.x - enemy.x) ** 2 + (self.player.y - enemy.y) ** 2) ** 0.5
                
                delta_points = self.points_base
                delta_points = delta_points * dist / 100 # REWARD MORE FOR KILLING DISTANT ENEMIES
                delta_points = delta_points / time_between_kills # REWARD MORE POINTS IF TIME BETWEEN KILLS DECREASES 
                delta_points = delta_points / self.difficulty # REWARD MORE POINTS IF DIFFICULTY IS LOWER
    
                delta_points = int(delta_points)
                delta_points = max(1, delta_points) # MINIMUM NUMBER OF POINTS IS 1
                
                self.player_points += delta_points


if __name__ == '__main__':
    game = GamePlay(difficulty=1, window=None)
    game.run()
