import arcade

from src.base.event import SimpleEvent
from src.base.registry import Registry, DeferredRegistry

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

WINDOW_TITLE = "survivor-project v0.1"


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

    def on_show_view(self):
        print("GameView")


def init():

    item_reg = Registry[str]("items")
    item_reg_def = DeferredRegistry[str](item_reg)

    reg_event = SimpleEvent()
    item_reg_def.set_register_event(reg_event)

    item_reg_def.register("item_1", lambda: "Item 1")
    item_reg_def.register("item_2", lambda: "Item 2")

    reg_event.trigger()

    print(item_reg.get("item_1"))

def main():

    init()

    window = arcade.Window()
    view = GameView()

    window.show_view(view)
    arcade.run()


if __name__ == '__main__':
    main()