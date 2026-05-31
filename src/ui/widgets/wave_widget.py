import arcade
import arcade.gui as gui

from settings.game_resources import GameResources


class WaveWidget(gui.UIAnchorLayout):
    def __init__(self):
        super().__init__()
        self.box = gui.UIBoxLayout(vertical=True, space_between=10, align="right")
        self.textures = arcade.load_spritesheet(GameResources.get("textures") / "ui" / "hud" / "wave_spritesheet.png").get_texture_grid((456,464),10,10)
        
        self.wave_number = 1
        
        self.wave_box = gui.UIBoxLayout(vertical=False, space_between=0)
        self.box.add(self.wave_box)

        self.add(self.box, anchor_x="right", anchor_y="top", align_x=-10, align_y=-10)
        self.update_display()

    def update_display(self):
        self.wave_box.clear()
        
        for char in str(self.wave_number):
            digit = int(char)
            # if order is 1,2,3...9,0:
            tex_index = digit - 1 if digit > 0 else 9
            
            widget = gui.UIImage(texture=self.textures[tex_index], width=50, height=100)
            self.wave_box.add(widget)

    def update_wave(self):
        self.wave_number += 1
        self.update_display()

