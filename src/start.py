from abc import ABC, abstractmethod
from typing import override, Set

import arcade

from src.base.event import EventBus, Event, Signal
from src.service.input import InputService

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

WINDOW_TITLE = "survivor-project v0.1"


class World:

    def __init__(self):
        self._entities = arcade.SpriteList()

    def add_entity(self, entity: "Entity"):
        self._entities.append(entity)

    def update_entities(self, delta_time: float):
        self._entities.update(delta_time)

    def draw_entities(self):
        self._entities.draw()


class EventHandler(ABC):

    def __init__(self, event_bus: EventBus):
        self._event_bus = event_bus

    @abstractmethod
    def subscribe_event(self):
        pass


class Entity(arcade.Sprite, EventHandler, ABC):

    def __init__(self, event_bus: EventBus):
        EventHandler.__init__(self, event_bus)


class


class Player(Entity):

    def __init__(self, event_bus: EventBus):
        super().__init__(event_bus)

    @override
    def subscribe_event(self):
        self._event_bus.dispatch(Event())


class GameView(arcade.View):

    def __init__(self, event_bus: EventBus, world: World, input_service: InputService):
        super().__init__()
        self._event_bus = event_bus
        self._world = world
        self._input = input_service

    def on_show_view(self):
        print("GameView")

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        self._input.register_input(symbol)

    def on_key_release(self, symbol: int, modifiers: int) -> bool | None:
        self._input.remove_input(symbol)

    def on_update(self, delta_time: float) -> bool | None:
        self._world.update_entities(delta_time)

    def on_draw(self) -> bool | None:
        self._world.draw_entities()


class PlayerAttackEvent(Event):

    def __init__(self, player: Player):
        super().__init__()
        self.player = player


def init(event_bus: EventBus):
    event_bus.subscribe(PlayerAttackEvent, lambda _: play_sound("player_attack.wav"))
    pass

def play_sound(sound: str):
    print(f"Playing sound: {sound}")

def main():

    gameplay_event_bus = EventBus()
    world = World()

    input_service = InputService()
    input_service.init()

    init(gameplay_event_bus)

    window = arcade.Window()
    view = GameView(EventBus(), world, input_service)
    player = Player(gameplay_event_bus)

    window.show_view(view)

    arcade.run()


if __name__ == '__main__':
    main()