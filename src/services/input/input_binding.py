from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import TypeVar, List, Dict

from src.services.input.game_input import InputSignature
from src.services.input.input_action import InputAction
from src.services.input.input_type import AxisInput, InputType
from src.services.input.util.composite_axis import CompositeAxis

T = TypeVar("T", bound=InputType)


@dataclass(frozen=True)
class ActiveInput:
    signature: InputSignature
    binding: "InputBinding"
    value: InputType


class InputTrigger(Enum):
    PRESS = auto()
    RELEASE = auto()
    HOLD = auto()
    CHANGE = auto()


class InputBinding(ABC):

    def __init__(self, input_action: InputAction, trigger: InputTrigger):
        self.input_action = input_action
        self.trigger = trigger

    @abstractmethod
    def input_signatures(self) -> List[InputSignature]:
        pass

    @abstractmethod
    def resolve_value(self, active_inputs: Dict[InputSignature, ActiveInput]) -> T:
        pass


class SimpleInputBinding(InputBinding):

    def __init__(self, input_signature: InputSignature, input_action: InputAction, trigger: InputTrigger):
        super().__init__(input_action, trigger)
        self.input_signature = input_signature

    def input_signatures(self) -> List[InputSignature]:
        return [self.input_signature]

    def resolve_value(self, active_inputs: Dict[InputSignature, ActiveInput]) -> T:

        if self.input_signature in active_inputs.keys():
            return active_inputs.get(self.input_signature).value

        return None


class CompositeAxisInputBinding(InputBinding):

    def __init__(self, composite_axis: CompositeAxis, input_action: InputAction):
        super().__init__(input_action, InputTrigger.HOLD)
        self.composite_axis = composite_axis

    def input_signatures(self) -> List[InputSignature]:
        return self.composite_axis.signatures()

    def resolve_value(self, active_inputs: Dict[InputSignature, ActiveInput]) -> AxisInput:
        return self.composite_axis.resolve(active_inputs.keys())