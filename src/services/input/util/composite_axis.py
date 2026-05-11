from typing import List

from src.services.input.game_input import InputSignature
from src.services.input.input_type import AxisInput


class CompositeAxis:

    def __init__(self, up: InputSignature, down: InputSignature, left: InputSignature, right: InputSignature):
        self.up = up
        self.down = down
        self.left = left
        self.right = right

    def resolve(self, active_signatures: List[InputSignature]) -> AxisInput:

        x, y = 0.0, 0.0

        if self.up in active_signatures:
            y += 1
        if self.down in active_signatures:
            y -= 1

        if self.left in active_signatures:
            x -= 1
        if self.right in active_signatures:
            x += 1

        return AxisInput(x, y)

    def contains(self, signature: InputSignature) -> bool:

        return (
            signature == self.up or
            signature == self.down or
            signature == self.left or
            signature == self.right
        )

    def signatures(self) -> List[InputSignature]:
        return [self.up, self.down, self.left, self.right]