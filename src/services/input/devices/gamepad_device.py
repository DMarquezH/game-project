from src.services.input.game_input import GameInput
from src.services.input.input_type import EmptyInput, AxisInput, AnalogInput
from src.services.input.settings.registered_input_devices import RegisteredInputDevice


class GamepadInputSource:
    BUTTON = "button"
    STICK = "stick"
    TRIGGER = "trigger"


class GamepadInputDevice:

    @staticmethod
    def from_button(button_code: str) -> GameInput[EmptyInput]:

        return GameInput[EmptyInput](
            device=RegisteredInputDevice.GAMEPAD.value,
            source=f"{GamepadInputSource.BUTTON}.{button_code}",
            value=EmptyInput()
        )

    @staticmethod
    def from_stick(stick: str, x: float, y: float) -> GameInput[AxisInput]:

        return GameInput[AxisInput](
            device=RegisteredInputDevice.GAMEPAD.value,
            source=f"{GamepadInputSource.STICK}.{stick}",
            value=AxisInput(x, y)
        )

    @staticmethod
    def from_trigger(trigger: str, value: float) -> GameInput[AnalogInput]:

        return GameInput[AnalogInput](
            device=RegisteredInputDevice.GAMEPAD.value,
            source=f"{GamepadInputSource.TRIGGER}.{trigger}",
            value=AnalogInput(value)
        )