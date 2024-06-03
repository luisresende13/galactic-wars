'''
TRABALHO FINAL
LABORATÓRIO DE JOGOS
2024/1
'''

import time

from PPlay.window import Window
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse
from PPlay.sprite import Sprite

from game_play_v5 import GamePlay

from modules.menu import Menu
from modules.option import MenuOption
from modules.player import Player
from modules.shot import Shot
from modules.image_util import get_screen_size, resize_background

difficulty_levels = {
    'FÁCIL': 1,
    'MÉDIO': 2,
    'DIFÍCIL': 3,
}

class Game:
    def __init__(self, background_path='imgs/backgrounds/ai/ai-home-8.jpg'):
        screen_width, screen_height = get_screen_size()        
        self.window = Window(screen_width, screen_height)
        self.window.set_title('Menu')
        self.keyboard = self.window.get_keyboard()
        self.mouse = Mouse()
        self.current_screen = 'MENU'
        self.selected_difficulty = 1

        # Resize background image to fit the shape of the screen
        background_resized_path = 'imgs/backgrounds/resized.jpg'
        resize_background(background_path, background_resized_path)
        self.background = GameImage(background_resized_path)

        ww = self.window.width
        wh = self.window.height
        
        option_ = Sprite('imgs/button.png')
        optw = option_.width
        opth = option_.height

        menu_x = ww / 2 - optw / 2
        
        menu_options = [
            MenuOption(menu_x, 330, "JOGAR"),
            MenuOption(menu_x, 330 + 20 + 64, "DIFICULDADE"),
            MenuOption(menu_x, 330 + 2 * 20 + 2 * 64, "RANKING"),
            MenuOption(menu_x, 330 + 3 * 20 + 3 * 64, "SAIR")
        ]
        
        difficulty_options = [
            MenuOption(menu_x, 330, "FÁCIL"),
            MenuOption(menu_x, 330 + 20 + 64, "MÉDIO"),
            MenuOption(menu_x, 330 + 2 * 20 + 2 * 64, "DIFÍCIL"),
        ]

        self.menu = Menu(menu_options)
        self.difficulty_menu = Menu(difficulty_options)

    def run(self):
        while True:
            self.window.update()

            self.window.set_background_color((255, 255, 255))
            self.background.draw()
            
            if self.current_screen == "MENU":
                if self.keyboard.key_pressed("ESC"):
                    break

                self.menu.draw(self.window)

                screen_name = self.menu.handle_click()
                if screen_name is not None:
                    self.current_screen = screen_name
    
                    # Wait mouse click to finish
                    while self.mouse.is_button_pressed(1):
                        time.sleep(0.2) # busy waiting
                    
            elif self.current_screen == "JOGAR":
                game_play = None
                game_play = GamePlay(self.selected_difficulty, self.window)
                game_play.run()
                
                self.current_screen = 'MENU'
                
            elif self.current_screen == "DIFICULDADE":
                self.difficulty_menu.draw(self.window)

                selected_difficulty_name = self.difficulty_menu.handle_click()
                if selected_difficulty_name is not None:
                    self.selected_difficulty = difficulty_levels[selected_difficulty_name]
                    self.current_screen = 'MENU'

                    # Wait mouse click to finish
                    while self.mouse.is_button_pressed(1):
                        time.sleep(0.2) # busy waiting
                
                if self.keyboard.key_pressed('esc'):
                    self.current_screen = 'MENU'
                
            elif self.current_screen == "RANKING":
                self.current_screen = "MENU"
            
            elif self.current_screen == "SAIR":
                break
            
                













