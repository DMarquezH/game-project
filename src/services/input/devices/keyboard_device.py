from services.input.game_input import GameInput, InputSignature
from services.input.input_type import EmptyInput
from services.input.settings.registered_input_devices import RegisteredInputDevice


class KeyboardInputSource:
    KEY = "key"


class KeyboardInputDevice:

    @staticmethod
    def source_from_key(key_code: int) -> str:
        return f"{KeyboardInputSource.KEY}.{key_code}"

    @staticmethod
    def signature_from_key(key_code: int) -> InputSignature:

        return InputSignature(
            RegisteredInputDevice.KEYBOARD.value,
            KeyboardInputDevice.source_from_key(key_code)
        )

    @staticmethod
    def from_key(key_code: int) -> GameInput[EmptyInput]:

        return GameInput[EmptyInput](
            device=RegisteredInputDevice.KEYBOARD.value,
            source=KeyboardInputDevice.source_from_key(key_code),
            value=EmptyInput()
        )