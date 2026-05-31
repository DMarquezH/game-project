import arcade
import arcade.gui as gui

from settings.game_resources import GameResources


class WaveWidget(gui.UIAnchorLayout):
    def __init__(self):
        super().__init__()
        self.box = gui.UIBoxLayout(vertical=True, space_between=10, align="right")
        self.textures = arcade.load_spritesheet(GameResources.get("textures") / "ui" / "hud" / "wave_spritesheet.png").get_texture_grid((456,464),10,30)
        self.active_texture = 0
        self.widget = gui.UIImage(texture=self.textures[self.active_texture],width=100,height=100)

        self.box.add(self.widget)

        self.add(self.box, anchor_x="right", anchor_y="top", align_x=-10, align_y=-10)

    def update_wave(self):
        if self.active_texture< 29: self.active_texture += 1
        self.widget.texture = self.textures[self.active_texture]

