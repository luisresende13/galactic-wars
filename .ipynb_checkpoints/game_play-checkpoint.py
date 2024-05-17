import time
from PPlay.window import Window
from PPlay.gameimage import GameImage
from player import Player
from shot import Shot

class GamePlay:
    def __init__(self, difficulty):
        self.difficulty = difficulty

        self.speed_player = 400 / self.difficulty
        self.speed_shot = 600 / self.difficulty
        self.shot_min_rate = 6 / self.difficulty # shots per second
        self.last_shot_time = time.time()

        self.window = Window(1280, 720)
        self.window.set_title("Game Play")
        self.keyboard = self.window.get_keyboard()
        self.background = GameImage("imgs/backgrounds/deep_space_gray_1280x720.png")
            
        player_x = self.window.width / 2
        player_y = self.window.height * 13 / 16 # bottom of the self.window
        
        self.player = Player(player_x, player_y, 'imgs/ships/player.png')
    
        self.shots = []

    def run(self):
    
        while True:
            if self.keyboard.key_pressed("ESC"):
                break
    
            if self.keyboard.key_pressed("right"):
                if self.player.sprite.x + self.player.sprite.width < self.window.width:
                    move_x = self.speed_player  * self.window.delta_time()
                    self.player.move(move_x, 0)
                    
            if self.keyboard.key_pressed("left"):
                if self.player.sprite.x > 0:
                    move_x = - 1 * self.speed_player  * self.window.delta_time()
                    self.player.move(move_x, 0)

            if self.keyboard.key_pressed("down"):
                if self.player.sprite.y + self.player.sprite.height < self.window.height:
                    move_y = self.speed_player  * self.window.delta_time()
                    self.player.move(0, move_y)
                    
            if self.keyboard.key_pressed("up"):
                if self.player.sprite.y > 0:
                    move_y = - 1 * self.speed_player  * self.window.delta_time()
                    self.player.move(0, move_y)

            if self.keyboard.key_pressed("space"):
                time_diff = time.time() - self.last_shot_time
                if time_diff > 1 / self.shot_min_rate:
                    self.last_shot_time = time.time()
                    
                    shot_x = self.player.sprite.x + self.player.sprite.width / 2
                    shot_y = self.player.sprite.y
                    
                    new_shot = Shot(shot_x, shot_y, 'imgs/shots/shot-fire-3x-rot-final.png')
                    self.shots.append(new_shot)
                    print(f'NEW SHOT... N-SHOTS: {len(self.shots)}')
    
            move_shot_y = - 1 * self.speed_shot * self.window.delta_time()
            for shot in self.shots:
                shot.move(0, move_shot_y)
    
            remove_shot_index = []
            for i, shot in enumerate(self.shots):
                if shot.sprite.y <= 0:
                    remove_shot_index.append(i)
    
            for i in remove_shot_index:
                del self.shots[i]

            # Draw elements
            
            self.background.draw()
            
            for shot in self.shots:
                shot.draw()
                
            self.player.draw()
            self.window.update()

if __name__ == '__main__':
    game = GamePlay(difficulty=1)
    game.run()