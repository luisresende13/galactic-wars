'''
TO-DO:

dontpad.com/invaders-Luciano

--------- Instructions ---------
1. SHIP MOVES HORIZONTALLY AND STOPS AT THE WALL
2. SHOOTING:
    2.1 Create empty list of shots
    2.2 If (space): Create new shot; position sprite; append to list;
    2.3 Later, run through the list and draw shots.
    2.4 Exclude shot if collide with end of screen

3. Create global variable difficulty (values: 1, 2, 3)
    3.1 Update difficulty on difficulty menu button click

4. Add reloading time:
    4.1 Shot needs to wait minimum time to be fired

'''

import time

from PPlay.window import Window
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse

from menu import Menu
from option import MenuOption
from player import Player
from shot import Shot
from game_play import GamePlay

difficulty_levels = {
    'FÁCIL': 1,
    'MÉDIO': 2,
    'DIFÍCIL': 3,
}

class Game:
    def __init__(self):
        self.window = Window(1280, 720)
        self.window.set_background_color((255, 255, 255))
        self.window.set_title('Menu')
        self.keyboard = self.window.get_keyboard()
        self.mouse = Mouse()
        self.background_image = GameImage('imgs/backgrounds/ai-home-8-1280x1280.jpg')
        self.current_screen = 'MENU'
        self.selected_difficulty = 1
        
        menu_options = [
            MenuOption(493, 330, "JOGAR"),
            MenuOption(493, 330 + 20 + 64, "DIFICULDADE"),
            MenuOption(493, 330 + 2 * 20 + 2 * 64, "RANKING"),
            MenuOption(493, 330 + 3 * 20 + 3 * 64, "SAIR")
        ]
        
        difficulty_options = [
            MenuOption(493, 330, "FÁCIL"),
            MenuOption(493, 330 + 20 + 64, "MÉDIO"),
            MenuOption(493, 330 + 2 * 20 + 2 * 64, "DIFÍCIL"),
        ]

        self.menu = Menu(menu_options)
        self.difficulty_menu = Menu(difficulty_options)

    def run(self):
        while True:
            self.window.update()

            self.window.set_background_color((255, 255, 255))
            self.background_image.draw()
            
            if self.current_screen == "MENU":
                                    
                self.menu.draw(self.window)

                screen_name = self.menu.handle_click()
                if screen_name is not None:
                    self.current_screen = screen_name
    
                    # Wait mouse click to finish
                    while self.mouse.is_button_pressed(1):
                        time.sleep(0.2) # busy waiting
                    
            elif self.current_screen == "JOGAR":
                game_play = GamePlay(difficulty=self.selected_difficulty)
                game_play.run()
                
                if self.keyboard.key_pressed('esc'):
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
            
                













