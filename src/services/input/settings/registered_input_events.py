from pyglet.math import Vec2

from services.event_service import BaseEvent


class ToggleFullscreenInputEvent(BaseEvent):
    pass


class PlayerMoveInputEvent(BaseEvent):

    def __init__(self, move_dir: Vec2):
        super().__init__()
        self.move_dir = move_dir


class PlayerAttackInputEvent(BaseEvent):

    def __init__(self, mouse_pos: Vec2):
        super().__init__()
        self.mouse_pos = mouse_pos


class TogglePauseInputEvent(BaseEvent):
    pass


class ToggleDebugInputEvent(BaseEvent):
    pass