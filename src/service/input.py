from typing import Callable, Set, ParamSpec, Generic, override

from src.base.event import Signal
from src.base.registry import Registry
from src.service.geometry import Vector2

P = ParamSpec("P")


class InputAction(Generic[P]):

    def __init__(self, key: str, context: str):
        self.key = key
        self._signal = Signal[P]()

    def add_listener(self, callback: Callable[P, None]):
        self._signal.connect(callback)

    def remove_listener(self, callback: Callable[P, None]):
        self._signal.disconnect(callback)


class InputContexts:
    DEFAULT = "default"
    GENERAL = "gameplay"
    GAMEPLAY = "gameplay"
    MENU = "menu"


class InputActions:

    TOGGLE_PAUSE = InputAction[[]]("toggle_pause", InputContexts.GENERAL)

    PLAYER_MOVE = InputAction[Vector2]("player_move", InputContexts.GAMEPLAY)
    PLAYER_INTERACT = InputAction[[]]("player_interact", InputContexts.GAMEPLAY)
    PLAYER_ATTACK = InputAction[[]]("player_attack", InputContexts.GAMEPLAY)

    MENU_MOVE = InputAction[[Vector2]]("menu_move", InputContexts.MENU)
    MENU_SELECT = InputAction[[]]("menu_select", InputContexts.MENU)
    MENU_BACK = InputAction[[]]("menu_back", InputContexts.MENU)


class InputService:

    def __init__(self):
        self._action_registry = Registry[InputAction]("base")
        self._active_inputs: Set[int] = set()

    def init(self):
        self._register_actions()

    def _register_actions(self):

        self.reg_action(InputActions.PLAYER_MOVE)
        self.reg_action(InputActions.PLAYER_INTERACT)
        self.reg_action(InputActions.PLAYER_ATTACK)

        self.reg_action(InputActions.TOGGLE_PAUSE)

        self._action_registry.freeze()

    def reg_action(self, action: InputAction):
        self._action_registry.register(action.key, action)

    def register_input(self, input_: int):
        self._active_inputs.add(input_)
        self._on_inputs_updated()

    def remove_input(self, input_: int):
        self._active_inputs.discard(input_)
        self._on_inputs_updated()

    def _on_inputs_updated(self):
        pass