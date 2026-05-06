from enum import Enum, auto

from src.input.game_input import GameInput, InputAction
from src.input.input_type import Axis, AxisMotion, MouseButton, MouseScroll, MouseDrag


class MouseInputSource(Enum):
    BUTTON = auto()
    WHEEL = auto()
    MOTION = auto()
    DRAG = auto()


class MouseInput:

    DEVICE_NAME = "mouse"

    @staticmethod
    def from_button(x: float, y: float, button: int, action: InputAction):

        return GameInput[MouseButton](
            MouseInput.DEVICE_NAME,
            MouseInputSource.BUTTON,
            MouseButton(x, y, button),
            action
        )

    @staticmethod
    def from_scroll(x: float, y: float, scroll_x: int, scroll_y: int):

        return GameInput[MouseScroll](
            MouseInput.DEVICE_NAME,
            MouseInputSource.WHEEL,
            MouseScroll(x, y, scroll_x, scroll_y),
            InputAction.SUBMIT
        )

    @staticmethod
    def from_motion(x: float, y: float, dx: float, dy: float):

        return GameInput[AxisMotion](
            MouseInput.DEVICE_NAME,
            MouseInputSource.MOTION,
            AxisMotion(x, y, dx, dy),
            InputAction.SUBMIT
        )

    @staticmethod
    def from_drag(x: float, y: float, dx: float, dy: float, button: int):

        return GameInput[MouseDrag](
            MouseInput.DEVICE_NAME,
            MouseInputSource.DRAG,
            MouseDrag(x, y, dx, dy, button),
            InputAction.SUBMIT
        )

    @staticmethod
    def from_area_interact(x: float, y: float, action: InputAction):

        return GameInput[Axis](
            MouseInput.DEVICE_NAME,
            MouseInputSource.MOTION,
            Axis(x, y),
            action
        )