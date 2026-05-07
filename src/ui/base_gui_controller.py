import arcade
import arcade.gui

class BaseGuiController():
    def __init__(self):
        self.manager = arcade.gui.UIManager()

    def enable(self):
        self.manager.enable()
    def disable(self):
        self.manager.disable()
    def draw(self):
        self.manager.draw()
