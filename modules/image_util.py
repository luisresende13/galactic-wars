import ctypes
import cv2

def get_screen_size():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screensize

def resize_background(background_path, background_resized_path):
    screen_width, screen_height = get_screen_size()
    background_image = cv2.imread(background_path)
    background_image_resized = cv2.resize(background_image, (screen_width, screen_height))
    cv2.imwrite(background_resized_path, background_image_resized)
