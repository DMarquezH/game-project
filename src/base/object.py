from typing import Callable

import arcade

from src.service.geometry import Vector2
from src.service.input import InputService, InputActions, InputAction


class Entity(arcade.Sprite):

    def __init__(self):
        super().__init__()


class ControllableEntity(Entity):

    def __init__(self, input_: InputService):
        super().__init__()
        self._input = input_
        self._action_subscriptions

    def _listen(self, action: InputAction, callback: Callable[..., None]):
        action.add_listener(callback)

    def dispose(self):
        pass


class Player(ControllableEntity):

    def __init__(self, input_: InputService):
        super().__init__(input_)
        self.subscribe_input_actions()

    def subscribe_input_actions(self):
        InputActions.PLAYER_MOVE.add_listener(self.on_move)
        InputActions.PLAYER_INTERACT.add_listener(self.on_interact)
        InputActions.PLAYER_ATTACK.add_listener(self.on_attack)

    def on_move(self, direction: Vector2):
        pass

    def on_interact(self):
        pass

    def on_attack(self):
        pass