from dataclasses import dataclass
from typing import TypeVar, Generic

from src.services.input.input_type import InputType

T = TypeVar("T", bound=InputType)


class GameInput(Generic[T]):

    def __init__(self, device: str, source: str, value: T):
        self.signature = InputSignature(device, source)
        self.value = value

    def __str__(self):
        return f"{self.signature}:{self.value}"

    def __eq__(self, other):

        if not isinstance(other, GameInput):
            return NotImplemented

        return (
                self.signature == other.signature and
                self.value == other.value
        )


@dataclass(frozen=True)
class InputSignature:

    device: str
    source: str

    def __str__(self):
        return f"{self.device}.{self.source}".lower()

    def __eq__(self, other):

        if not isinstance(other, InputSignature):
            return NotImplemented

        return (
            self.device == other.device and
            self.source == other.source
        )