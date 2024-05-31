import pyautogui

button_names = {
    1: 'left',
    2: 'right',
    3: 'middle'
}

class Mouse:
    def __init__(self):
        pass
        
    def is_button_pressed(self, button=1):
        if button not in [1, 2, 3]:
            raise ValueError("Invalid mouse button. Please specify 1 (left), 2 (right), or 3 (middle).")
    
        button = button_names[button]
        return pyautogui.mouseInfo().get(button + 'Button')

if __name__ == '__main__':
    import time
    mouse = Mouse()
    i = 0
    while not mouse.is_button_pressed(button=1):
        i += 1
        print(f'mouse not pressed: {i}')
        time.sleep(1)

    i = 0
    while mouse.is_button_pressed(button=1):
        i += 1
        print(f'mouse pressed: {i}')

    print(f'mouse pressed finished: {i}/{i}')
