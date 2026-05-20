import arcade.gui
import arcade.gui as gui


class ButtonWrapper(gui.UIFlatButton):
    def __init__(self, widget:gui.UIWidget | None =None, action= None):
        width, height = 100,100
        padding = 20
        self.action = action
        if widget:
            width,height = int(widget.width) + padding , int(widget.height) + padding

        super().__init__(width=width,height=height)
        if widget:
            self.add(child=widget,anchor_x="center",anchor_y="center")
    def on_click(self, event: gui.UIMousePressEvent):
        if self.action:
            self.action()