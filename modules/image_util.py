import ctypes
import cv2

def get_screen_size():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screensize

def resize_background(background_path, background_resized_path, keep_width=False, keep_height=False, new_width=None, new_height=None):
    screen_width, screen_height = get_screen_size()
    background_image = cv2.imread(background_path)
    new_shape = [screen_width, screen_height]
    if keep_width:
        new_shape[0] = background_image.shape[0]
    if keep_height:
        new_shape[1] = background_image.shape[1]
    if new_width is not None:
        new_shape[0] = new_width
    if new_height is not None:
        new_shape[1] = new_height

    background_image_resized = cv2.resize(background_image, new_shape)
    cv2.imwrite(background_resized_path, background_image_resized)
