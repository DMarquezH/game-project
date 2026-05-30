import arcade
import arcade.gui
from pathlib import Path

class ScoreWidget(arcade.gui.UIBoxLayout):
    def __init__(self, image:Path, text:str,scale = 1):
        super().__init__(vertical=False,space_between=10)

        self.image_texture = None
        self.image_texture = arcade.load_texture(image)
        self.image_widget = arcade.gui.UIImage(texture=self.image_texture,width=self.image_texture.width/4*scale,height=self.image_texture.height/4*scale)

        self.label_widget = arcade.gui.UILabel(text= str(text),font_size=18*scale,font_name="Black Ops One")

        self.add(self.image_widget)
        self.add(self.label_widget)

        self.width = self.image_widget.width + self.label_widget.width + self._space_between
        self.height = self.image_widget.height

        self.widget_stat = None
    def set_text(self,text:str):
        self.label_widget.text = text