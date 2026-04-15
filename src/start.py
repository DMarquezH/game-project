import arcade

from src.base.event import EventBus, Event

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

WINDOW_TITLE = "survivor-project v0.1"

EVENT_BUS = EventBus()


class KeyPressedEvent(Event):

    def __init__(self, symbol: int, modifiers: int):
        super().__init__()

        self.symbol = symbol
        self.modifiers = modifiers


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

    def on_show_view(self):
        print("GameView")

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        EVENT_BUS.dispatch(KeyPressedEvent(symbol, modifiers))


def init():
    EVENT_BUS.subscribe(KeyPressedEvent, lambda e: print(f"Key pressed: {e.symbol}"))

def main():

    init()

    window = arcade.Window()
    view = GameView()

    window.show_view(view)
    arcade.run()


if __name__ == '__main__':
    main()