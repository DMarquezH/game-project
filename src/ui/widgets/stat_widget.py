import arcade
import arcade.gui as gui
import json

from settings.game_resources import GameResources
from ui.widgets.score_widget import ScoreWidget
from world.systems.combat.entity_stats import EntityStats


class StatWidget(gui.UIAnchorLayout):
    def __init__(self,stats:EntityStats):
        super().__init__()

        self.box1 = arcade.gui.UIBoxLayout(vertical= True, space_between=10,align="left")
        self.box2 = arcade.gui.UIBoxLayout(vertical= True, space_between=10,align="left")
        self.data = json.load(open(GameResources.get("data")/"items.json"))
        for i in range(1,7):
            item = self.data[i]
            widget = ScoreWidget(image= GameResources.get("textures") / item["texture"],text=int(stats.get(EntityStats.resolve(item["stat"]))),scale=0.8)
            widget.widget_stat = item["stat"]
            self.box1.add(widget)
        for i in range(7,12):
            item = self.data[i]
            widget = ScoreWidget(image=GameResources.get("textures") / item["texture"],text=int(stats.get(EntityStats.resolve(item["stat"]))),scale=0.8)
            widget.widget_stat = item["stat"]
            self.box2.add(widget)

        self.add(self.box1, anchor_x="left", anchor_y="center", align_x=10, align_y=-50)
        self.add(self.box2,anchor_x="right",anchor_y="center", align_x=-10, align_y=-30)

    def update_stats(self,stats:EntityStats):
        for elem1,elem2 in zip(self.box1.children,self.box2.children):
            elem1.set_text(int(stats.get(EntityStats.resolve(elem1.widget_stat))))
            elem2.set_text(int(stats.get(EntityStats.resolve(elem2.widget_stat))))
