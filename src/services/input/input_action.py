from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.services.event_service import EventBus
from src.services.input.game_input import GameInput
from src.services.input.input_type import InputType

T = TypeVar("T", bound=InputType)


class InputAction(ABC):

    @abstractmethod
    def activate(self, event_bus: EventBus, input_value: T):
        pass