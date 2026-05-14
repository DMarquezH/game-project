from abc import ABC, abstractmethod
from typing import TypeVar

from services.event_service import EventBus
from services.input.input_type import InputType

T = TypeVar("T", bound=InputType)


class InputAction(ABC):

    @abstractmethod
    def activate(self, event_bus: EventBus, input_value: T):
        pass