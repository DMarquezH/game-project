from pyglet.math import Vec2

from src.services.event_service import BaseEvent


class PlayerMoveInputEvent(BaseEvent):

    def __init__(self, move_dir: Vec2):
        super().__init__()
        self.move_dir = move_dir


class PlayerAttackInputEvent(BaseEvent):

    def __init__(self, mouse_pos: Vec2):
        super().__init__()
        self.mouse_pos = mouse_pos


class TogglePauseInputEvent(BaseEvent):

    def __init__(self):
        super().__init__()


class ToggleDebugInputEvent(BaseEvent):

    def __init__(self):
        super().__init__()