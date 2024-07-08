import pygame
import time
from PPlay.sprite import Sprite

class Animation:
    def __init__(self, images, duration=10):
        if not len(images):
            raise Exception('ERROR! CANNOT INITIALIZE ANIMATION WITH EMPTY LIST OF IMAGES')
            
        self.sprites = [Sprite(image_path) for image_path in images]
        self.duration = duration
        self.start_time = None
        self.fid = 0
        self.sprite = self.sprites[self.fid]
        self.position = (self.sprite.x, self.sprite.y)
        self.is_finished = False

    def start(self):
        self.start_time = time.time()
        self.fid = 0
        self.sprite = self.sprites[self.fid]
        self.sprite.x, self.sprite.y = self.position
        self.is_finished = False

    def update(self):
        if self.start_time is None:
            return
        
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        total_frames = len(self.sprites)
        
        if elapsed_time >= self.duration:
            self.is_finished = True
            self.fid = total_frames - 1
        else:
            frame_duration = self.duration / total_frames
            self.fid = int(elapsed_time // frame_duration) #  % total_frames

        self.sprite = self.sprites[self.fid]
        self.sprite.x, self.sprite.y = self.position

    def move(self, x, y):
        self.sprite.set_position(x, y)
        self.position = (x, y)
        
    def draw(self):
        self.sprite.draw()

# Example usage:
if __name__ == "__main__":    
    # Initialize pygame and create a window
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Custom Animation Example")
    
    # Load a list of images for the animation
    import os
    base_path = 'imgs/ships/player/final/rotation/'
    images = [base_path + path for path in sorted(os.listdir())]
    
    # Create a CustomAnimation instance with the images and a duration of 2 seconds
    animation = Animation(images, 5.0)
    
    # Start the animation
    animation.start()
    
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                
        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the animation
        animation.update()
        animation.move(animation.sprite.x + 10, animation.sprite.y + 10)
        animation.draw()
        
        # Update the display
        pygame.display.flip()
    
    pygame.quit()
