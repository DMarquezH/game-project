from abc import ABC, abstractmethod

from pyglet.math import Vec2


class InputType(ABC):

    @abstractmethod
    def __str__(self) -> str:
        pass

    def __repr__(self):
        return self.__str__()


class EmptyInput(InputType):

    STRING_VALUE = "none"

    def __str__(self) -> str:
        return self.STRING_VALUE


class AnalogInput(InputType):

    MIN = 0.0
    MAX = 1.0

    DEC_RND = 4

    def __init__(self, value: float):
        self.value = round(AnalogInput.clamp(value), self.DEC_RND)

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    def clamp(value: float) -> float:
        return max(AnalogInput.MIN, min(value, AnalogInput.MAX))


class AxisInput(InputType):

    DEC_RND = 4

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def get_vector(self) -> Vec2:
        return Vec2(self.x, self.y)

    def __str__(self) -> str:
        return f"({round(self.x, self.DEC_RND)},{round(self.y, self.DEC_RND)})"


class AxisMotionInput(AxisInput):

    def __init__(self, x: float, y: float, dx: float, dy: float):
        super().__init__(x, y)
        self.dx = dx
        self.dy = dy

    def get_start_vector(self) -> Vec2:
        return Vec2(self.x - self.dx, self.y - self.dy)

    def __str__(self) -> str:

        pos = str(super())
        dif = f"({round(self.x, self.DEC_RND)},{round(self.y, self.DEC_RND)})"

        return f"[{pos},{dif}]"


class MouseScrollInput(AxisInput):

    def __init__(self, x: float, y: float, scroll_x: int, scroll_y: int):
        super().__init__(x, y)
        self.scroll_x = scroll_x
        self.scroll_y = scroll_y

    def __str__(self) -> str:

        pos = str(super())
        scroll = f"({self.scroll_x},{self.scroll_y})"

        return f"[{pos},{scroll}]"