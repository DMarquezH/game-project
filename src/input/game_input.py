from dataclasses import dataclass
from enum import Enum, auto
from typing import TypeVar, Generic

T = TypeVar("T")


class InputAction(Enum):
    PRESS = auto()
    RELEASE = auto()
    SUBMIT = auto()


@dataclass
class GameInput(Generic[T]):

    def __init__(self, device: str, source: str, value: T, action: InputAction):
        self.device = device
        self.source = source
        self.value = value
        self.action = action