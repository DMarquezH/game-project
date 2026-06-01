import arcade
import arcade.gui

from ui.widgets.base_button import BaseButton
from pathlib import Path
from services.event_service import EventBus

class GridButtons(arcade.gui.UIAnchorLayout):
    """
    UI layout component that organizes the main menus buttons

    Args:
        * button_list (list[dict]): list of buttons with dictionaries with its characteristics:
            -"sheet"(str): path to the spritesheet with the 2 different styles ([0]->Normal, [1]->Hovered)
            -"action"(callback): Function executable when the button is pressed
            -"width"(int): width of a single image of the sheet button
            -"height"(int): height of a single image of the sheet button
            -"columns"(int): number of columns of sheet button
            -"count"(int): number of images of sheet button (Only 2 are going to be considered)
        * "space_between"(int): spaces between buttons [Default=0]
        * "position_x"(str): Screen location x -> "center","left","right" [Default="center"]
        * "position_y"(str): Screen location y ->"center","bottom","top" [Default="center"]


    """
    def __init__(self, button_list:list[dict], background:Path=None, space_between:int=0, position_x="center", position_y="center", event_bus: EventBus = None,scale=1):
        super().__init__()
        box_layout = arcade.gui.UIBoxLayout(space_between=space_between)
        for button in button_list:
            boton = BaseButton(
                sheet=button["sheet"],
                event_bus=event_bus,
                action=button["action"],
                image_width=button.get("width",0),
                image_height=button.get("height",0),
                columns=button.get("columns",0),
                count=button.get("count",0),
                scale=scale
            )
            box_layout.add(boton)
        if background:
            tx = arcade.load_texture(background)
            imageUI = arcade.gui.UIImage(texture=tx)
            self.add(child=imageUI,anchor_x=position_x,anchor_y=position_y)
        self.add(child=box_layout,anchor_x=position_x,anchor_y=position_y,)