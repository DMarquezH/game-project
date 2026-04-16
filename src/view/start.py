import arcade

from src.base.event import EventBus
from src.service.input import InputService, InputActions

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

WINDOW_TITLE = "survivor-project v0.1"


class GameView(arcade.View):

    def __init__(self, event_bus: EventBus, input_service: InputService):
        super().__init__()
        self._event_bus = event_bus
        self._input = input_service

    def on_show_view(self):
        print("GameView")

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        self._input.register_input(symbol)

    def on_key_release(self, symbol: int, modifiers: int) -> bool | None:
        self._input.remove_input(symbol)

    def on_update(self, delta_time: float) -> bool | None:
        pass

    def on_draw(self) -> bool | None:
        pass


def main():

    input_service = InputService()

    window = arcade.Window()
    view = GameView(EventBus(), input_service)

    window.show_view(view)
    arcade.run()


if __name__ == '__main__':
    main()