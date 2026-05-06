from enum import Enum, auto

from src.input.game_input import GameInput, InputAction


class KeyboardInputSource(Enum):
    KEY = auto()


class KeyboardInput:

    DEVICE_NAME = "keyboard"

    @staticmethod
    def from_key(key: int, action: InputAction):

        return GameInput(
            KeyboardInput.DEVICE_NAME,
            KeyboardInputSource.KEY,
            key,
            action
        )