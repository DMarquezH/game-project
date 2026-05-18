from pyglet.math import Vec2

from services.event_service import BaseEvent


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

class ViewportChangedEvent(BaseEvent):  # no se si esto deberia ir aqui pero como no rompe nada pues lo dejo de mientras
    def __init__(self, width: float, height: float):
        super().__init__()
        self.width = width
        self.height = height