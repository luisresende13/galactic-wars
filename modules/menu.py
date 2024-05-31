from modules.option import MenuOption

class Menu:
    def __init__(self, options):
        self.options = options

    def draw(self, window):
        for option in self.options:
            option.draw(window)
            
    def handle_click(self):
        for option in self.options:
            if option.clicked():
                return option.text
