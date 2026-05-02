import math
from enum import Enum


class Vector2:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def length(self) -> float:
        return math.hypot(self.x, self.y)

    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y

    def angle(self) -> float:
        return math.atan2(self.y, self.x)

    def rotate(self, angle: float) -> None:

        if  angle == 0: return

        sin = math.sin(angle)
        cos = math.cos(angle)

        x, y = self.x, self.y

        self.x = x * cos - y * sin
        self.y = x * sin + y * cos

    def rotated(self, angle: float) -> "Vector2":

        if angle == 0: return self.copy()

        sin = math.sin(angle)
        cos = math.cos(angle)

        return Vector2(
            self.x * cos - self.y * sin,
            self.x * sin + self.y * cos
        )

    def normalize(self) -> None:

        length = self.length()

        if length != 0:
            self.x /= length
            self.y /= length

    def normalized(self) -> "Vector2":

        length = self.length()

        if length == 0:
            return Vector2.zero()

        return Vector2(
            self.x / length,
            self.y / length
        )

    def clamp(self, min_length: float | None = None, max_length: float | None = None) -> None:

        if min_length is None and max_length is None: return

        length = self.length()
        self.normalize()

        if length < min_length:
            self.x *= min_length
            self.y *= min_length

        elif length > max_length:
            self.x *= max_length
            self.y *= max_length

    def clamped(self, min_length: float | None = None, max_length: float | None = None) -> "Vector2":

        copy = self.copy()

        if min_length is None and max_length is None: return self.copy()

        length = copy.length()
        copy.normalize()

        if length < min_length:
            return copy * min_length

        if length > max_length:
            return copy * max_length

        return copy

    def perpendicular(self, opposite=False) -> "Vector2":
        return Vector2(-self.y, self.x) if not opposite else Vector2(self.y, -self.x)

    def reflect(self, normal: "Vector2") -> "Vector2":
        return self - normal * (2 * Vector2.dot(self, normal))

    def distance_to(self, other: "Vector2") -> "Vector2":
        return other - self

    def copy(self) -> "Vector2":
        return Vector2(self.x, self.y)

    def to_tuple(self) -> tuple:
        return self.x, self.y

    def is_zero(self) -> bool:
        return self.x == 0 and self.y == 0

    @staticmethod
    def dot(v1: "Vector2", v2: "Vector2") -> float:
        return v1.x * v2.x + v1.y * v2.y

    @staticmethod
    def cross(v1: "Vector2", v2: "Vector2") -> float:
        return v1.x * v2.y - v1.y * v2.x

    @staticmethod
    def angle_between(v1: "Vector2", v2: "Vector2") -> float:
        return math.atan2(Vector2.cross(v1, v2), Vector2.dot(v1, v2))

    @staticmethod
    def distance(v1: "Vector2", v2: "Vector2") -> "Vector2":
        return v2 - v1

    @staticmethod
    def projection(v1: "Vector2", v2: "Vector2") -> "Vector2":

        length_2_sqd = v2.length_squared()

        if length_2_sqd == 0:
            return Vector2.zero()

        scale = Vector2.dot(v1, v2) / length_2_sqd
        return v2 * scale

    @staticmethod
    def lerp(a: "Vector2", b: "Vector2", t: float) -> "Vector2":
        return a + (b - a) * t

    @staticmethod
    def zero() -> "Vector2":
        return Vector2(0, 0)

    @staticmethod
    def from_dir(direction: "Direction") -> "Vector2":
        return Vector2(*direction.value)

    @staticmethod
    def from_angle(angle: float) -> "Vector2":
        return Vector2(math.cos(angle), math.sin(angle))

    def __add__(self, other):

        if not isinstance(other, Vector2):
            return NotImplemented

        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):

        if not isinstance(other, Vector2):
            return NotImplemented

        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):

        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)

        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):

        if not isinstance(other, (int, float)):
            return NotImplemented

        return Vector2(self.x / other, self.y / other)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    def __eq__(self, other):

        if not isinstance(other, Vector2):
            return False

        return self.x == other.x and self.y == other.y

    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, index):

        if index == 0:
            return self.x

        elif index == 1:
            return self.y

        else:
            raise IndexError("Vector2 index out of range")


class Direction(Enum):
    NORTH = (0, 1)
    SOUTH = (0, -1)
    EAST = (1, 0)
    WEST = (-1, 0)