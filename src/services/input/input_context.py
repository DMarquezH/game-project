from typing import Dict

from src.services.input.game_input import InputSignature
from src.services.input.input_binding import InputBinding


class InputContext:

    def __init__(self, name: str):
        self.name = name
        self.bindings: Dict[InputSignature, InputBinding] = {}

    def bind(self, binding: InputBinding):

        for signature in binding.input_signatures():
            self.bindings[signature] = binding

    def unbind(self, binding: InputBinding):

        for signature in binding.input_signatures():
            self.bindings.pop(signature, None)