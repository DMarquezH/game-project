from src.input.game_input import GameInput, InputAction


class KeyboardInputSource:
    KEY = "key"


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