from typing import Any

from pyglet.math import Vec2


class AxisInputMapper:

    def __init__(self, up: Any, down: Any, left: Any, right: Any):
        self.up = up
        self.down = down
        self.left = left
        self.right = right

    def get_vector(self, up: Any, down: Any, left: Any, right: Any):

        x, y = 0, 0

        if up == self.up:
            y += 1
        if down == self.down:
            y -= 1

        if right == self.right:
            x += 1
        if left == self.left:
            x -= 1

        return Vec2(x, y).normalize()


class Axis:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def get_vector(self) -> Vec2:
        return Vec2(self.x, self.y)


class AxisMotion(Axis):

    def __init__(self, x: float, y: float, dx: float, dy: float):
        super().__init__(x, y)
        self.dx = dx
        self.dy = dy

    def get_start_vector(self):
        return Vec2(self.x, self.y) - Vec2(self.dx, self.dy)


class MouseButton(Axis):

    def __init__(self, x: float, y: float, button: int):
        super().__init__(x, y)
        self.button = button


class MouseScroll(Axis):

    def __init__(self, x: float, y: float, scroll_x: int, scroll_y: int):
        super().__init__(x, y)
        self.scroll_x = scroll_x
        self.scroll_y = scroll_y


class MouseDrag(AxisMotion):

    def __init__(self, x: float, y: float, dx: float, dy: float, button: int):
        super().__init__(x, y, dx, dy)
        self.button = button