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

from PPlay.window import Window
from PPlay.gameimage import GameImage
from menu import Menu
from option import MenuOption
from player import Player
from shot import Shot

class Game:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.window = Window(self.width, self.height)
        self.window.set_background_color((255, 255, 255))
        self.window.set_title('SPACE INVADERS')
        self.keyboard = self.window.get_keyboard()
        self.current_screen = 'MENU'
        self.background_image = GameImage('imgs/backgrounds/background_l.png')
        # self.play_background_image = GameImage('imgs/backgrounds/space.png')
        # self.play_background_image.width = 1280
        # self.play_background_image.height = 720
        
        center_x = self.width / 2
        center_y = self.height / 2
        self.player = Player(center_x, center_y, 'imgs/ships/player.png')
        self.base_shot = Shot(center_x + 100, center_y, 'imgs/shots/shot-fire-3x-rot-final.png')

        menu_options = [
            MenuOption(493, 202, "JOGAR"),
            MenuOption(493, 202 + 20 + 64, "DIFICULDADE"),
            MenuOption(493, 202 + 2 * 20 + 2 * 64, "RANKING"),
            MenuOption(493, 202 + 3 * 20 + 3 * 64, "SAIR")
        ]
        
        match_options = [
            MenuOption(493, 202, "JOGAR"),
        ]

        difficulty_options = [
            MenuOption(493, 202, "FÁCIL"),
            MenuOption(493, 202 + 20 + 64, "MÉDIO"),
            MenuOption(493, 202 + 2 * 20 + 2 * 64, "DIFÍCIL"),
        ]

        self.menu = Menu(menu_options)
        self.match = Menu(match_options)
        self.difficulty = Menu(difficulty_options)

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
                    
            elif self.current_screen == "JOGAR":
                # self.play_background_image.draw()
                
                self.match.draw(self.window)
                self.player.draw()
                self.base_shot.draw()
                
                if self.keyboard.key_pressed('esc'):
                    self.current_screen = 'MENU'
                
            elif self.current_screen == "DIFICULDADE":
                self.difficulty.draw(self.window)
                
                if self.keyboard.key_pressed('esc'):
                    self.current_screen = 'MENU'
                
            elif self.current_screen == "RANKING":
                self.current_screen = "MENU"
            
            elif self.current_screen == "SAIR":
                break
            
                













