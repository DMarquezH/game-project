from src.services.input.game_input import GameInput, InputSignature
from src.services.input.input_type import AxisInput, AxisMotionInput, MouseScrollInput
from src.services.input.settings.registered_input_devices import RegisteredInputDevice


class MouseInputSource:
    BUTTON = "button"
    SCROLL = "scroll"
    MOTION = "motion"
    DRAG = "drag"


class MouseInputDevice:

    @staticmethod
    def source_from_button(button_code: int) -> str:
        return f"{MouseInputSource.BUTTON}.{button_code}"

    @staticmethod
    def source_from_drag(button_code: int) -> str:
        return f"{MouseInputSource.DRAG}.{button_code}"

    @staticmethod
    def signature_from_button(button_code: int) -> InputSignature:

        return InputSignature(
            RegisteredInputDevice.MOUSE.value,
            MouseInputDevice.source_from_button(button_code)
        )

    @staticmethod
    def signature_from_scroll() -> InputSignature:

        return InputSignature(
            RegisteredInputDevice.MOUSE.value,
            MouseInputSource.SCROLL
        )

    @staticmethod
    def signature_from_motion() -> InputSignature:

        return InputSignature(
            RegisteredInputDevice.MOUSE.value,
            MouseInputSource.MOTION
        )

    @staticmethod
    def signature_from_drag(button_code: int) -> InputSignature:

        return InputSignature(
            RegisteredInputDevice.MOUSE.value,
            MouseInputDevice.source_from_drag(button_code)
        )

    @staticmethod
    def from_button(button_code: int, x: float, y: float) -> GameInput[AxisInput]:

        return GameInput[AxisInput](
            device=RegisteredInputDevice.MOUSE.value,
            source=MouseInputDevice.source_from_button(button_code),
            value=AxisInput(x, y)
        )

    @staticmethod
    def from_scroll(x: float, y: float, scroll_x: int, scroll_y: int) -> GameInput[MouseScrollInput]:

        return GameInput[MouseScrollInput](
            device=RegisteredInputDevice.MOUSE.value,
            source=MouseInputSource.SCROLL,
            value=MouseScrollInput(x, y, scroll_x, scroll_y)
        )

    @staticmethod
    def from_motion(x: float, y: float, dx: float, dy: float) -> GameInput[AxisMotionInput]:

        return GameInput[AxisMotionInput](
            device=RegisteredInputDevice.MOUSE.value,
            source=MouseInputSource.MOTION,
            value=AxisMotionInput(x, y, dx, dy)
        )

    @staticmethod
    def from_drag(button_code: int, x: float, y: float, dx: float, dy: float) -> GameInput[AxisMotionInput]:

        return GameInput[AxisMotionInput](
            device=RegisteredInputDevice.MOUSE.value,
            source=MouseInputDevice.source_from_drag(button_code),
            value=AxisMotionInput(x, y, dx, dy)
        )