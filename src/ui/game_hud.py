import arcade
import arcade.gui
from src.ui.widgets.score_widget import ScoreWidget

class GameHud(arcade.gui.UIAnchorLayout):
    def __init__(self,config: list[dict]):
        super().__init__()
        self.box = arcade.gui.UIBoxLayout(vertical=True,space_between=10,align="left")
        self.widgets = {}
        for elementos in config:
            w = ScoreWidget(image=elementos['image'],text=elementos['text'])
            self.box.add(w)
            self.widgets[elementos["id"]] = w
        self.add(self.box,anchor_x="left",anchor_y="top",align_x=10,align_y=-10)
    def set_text(self,id_widget:str,text:str):
        if id_widget in self.widgets:
            self.widgets[id_widget].set_text(text)