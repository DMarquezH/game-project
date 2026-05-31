import arcade
import arcade.gui as gui
import time
from pathlib import Path
from services.event_service import EventBus
from settings.registered_gameplay_events import UIButtonClickEvent

class BaseButton(gui.UITextureButton):
    """
    A custom UI button that utilized a spritesheet image for a normal and hovered state

    Args:
        x(float): x position of the button. Defaults to 0
        y(float): y position of the button. Defaults to 0
        sheet(str): path to the spritesheet image
        image_width(int): width of a single frame of the spritesheet
        image_height(int): height of a single frame of the spritesheet
        count(int): number of images of the spritesheet to display, normally 2 (0->Normal, 1->Hover)
        action(callabe,optional): function to execute when te button is clicked. Defaults to None.
    """

    def __init__(self, sheet: Path, event_bus: EventBus = None, x=0, y=0, image_width=0, image_height=0, count=0, columns=0, action=None, scale=1, widget: gui.UIWidget | None =None):
        tex_normal = None
        tex_hover = None
        self.event_bus = event_bus
        if sheet.is_file():
            texture_grid = arcade.SpriteSheet(sheet)
            self.texture_list = texture_grid.get_texture_grid(size=(image_width,image_height),columns=columns,count=count)
            if len(self.texture_list) >= 2:
                tex_normal = self.texture_list[0]
                tex_hover = self.texture_list[1]

        super().__init__(width=image_width*scale,height=image_height*scale,x=x,y=y,texture=tex_normal,texture_hovered=tex_hover)
        self.action = action

        if widget:
            self.add(child=widget,anchor_x="center",anchor_y="center")

    def on_click(self, event: gui.UIMousePressEvent):
        """
        Event executed when the button is clicked

        Args:
            event(gui.UIMousePressEvent): the mouse event
        """
        if self.event_bus:
            self.event_bus.dispatch(UIButtonClickEvent())
        time.sleep(0.1)
        if self.action:
            self.action()