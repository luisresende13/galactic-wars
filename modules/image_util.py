# import ctypes
# import cv2

# def get_screen_size():
#     user32 = ctypes.windll.user32
#     screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
#     return screensize

# def resize_background(background_path, background_resized_path, keep_width=False, keep_height=False, new_width=None, new_height=None):
#     background_image = cv2.imread(background_path)
#     screen_width, screen_height = get_screen_size()
#     new_shape = [screen_width, screen_height]
#     if keep_width:
#         new_shape[0] = background_image.shape[0]
#     if keep_height:
#         new_shape[1] = background_image.shape[1]
#     if new_width is not None:
#         new_shape[0] = new_width
#     if new_height is not None:
#         new_shape[1] = new_height

#     background_image_resized = cv2.resize(background_image, new_shape)
#     cv2.imwrite(background_resized_path, background_image_resized)

import ctypes
import cv2
from PIL import Image

def get_screen_size():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screensize

# def resize_background(background_path, background_resized_path, keep_width=False, keep_height=False, new_width=None, new_height=None, keep_ratio=True):
#     # Load the image using Pillow
#     background_image = Image.open(background_path)
#     screen_width, screen_height = get_screen_size()
#     new_shape = [screen_width, screen_height]
#     if keep_width:
#         new_shape[0] = background_image.width
#     if keep_height:
#         new_shape[1] = background_image.height
#     if new_width is not None:
#         new_shape[0] = new_width
#     if new_height is not None:
#         new_shape[1] = new_height

#     # Resize the image with minimal quality loss
#     background_image_resized = background_image.resize((new_shape[0], new_shape[1]), Image.LANCZOS)
    
#     # Save the resized image
#     background_image_resized.save(background_resized_path, format='PNG')

def resize_background(background_path, background_resized_path, keep_width=False, keep_height=False, new_width=None, new_height=None, keep_ratio=False):
    # Load the image using Pillow
    background_image = Image.open(background_path)
    screen_width, screen_height = get_screen_size()
    
    # Calculate the new dimensions
    new_shape = [screen_width, screen_height]
    if keep_width:
        new_shape[0] = background_image.width
    if keep_height:
        new_shape[1] = background_image.height
    if new_width is not None:
        new_shape[0] = new_width
    if new_height is not None:
        new_shape[1] = new_height

    # Apply keep_ratio logic
    if keep_ratio:
        original_ratio = background_image.width / background_image.height
        if new_width is not None and new_height is None:
            # Calculate new height based on the width and original ratio
            new_shape[1] = int(new_shape[0] / original_ratio)
        elif new_height is not None and new_width is None:
            # Calculate new width based on the height and original ratio
            new_shape[0] = int(new_shape[1] * original_ratio)
        elif new_width is not None and new_height is not None:
            # Adjust dimensions to maintain the aspect ratio
            if new_shape[0] / original_ratio > new_shape[1]:
                new_shape[0] = int(new_shape[1] * original_ratio)
            else:
                new_shape[1] = int(new_shape[0] / original_ratio)
        else:
            # Adjust both dimensions to fit within the screen size while maintaining aspect ratio
            if screen_width / original_ratio > screen_height:
                new_shape[0] = int(screen_height * original_ratio)
                new_shape[1] = screen_height
            else:
                new_shape[0] = screen_width
                new_shape[1] = int(screen_width / original_ratio)
    
    # Resize the image
    resized_image = background_image.resize(new_shape)
    
    # Save the resized image
    resized_image.save(background_resized_path)
    print(f"Resized image saved to {background_resized_path}")

# # Example usage
# resize_background('path/to/your/background.png', 'path/to/your/background_resized.png')
