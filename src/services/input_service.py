from enum import Enum, auto

from src.core.service_container import Service


class Device(Enum):
    KEYBOARD = auto()
    MOUSE = auto()


class InputService(Service):

    def __init__(self):
        super().__init__("input")