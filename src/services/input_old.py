from typing import Callable, Set, ParamSpec, Generic, Dict

from src.core.registry import RegistryException
from services.event_service import Signal
from src.core.registry import TypeRegistry
from src.utils.geometry import Vector2

P = ParamSpec("P")


class InputAction(Generic[P]):

    def __init__(self, key: str):
        self.key = key
        self._signal = Signal[P]()

    def add_listener(self, callback: Callable[P, None]):
        self._signal.connect(callback)

    def remove_listener(self, callback: Callable[P, None]):
        self._signal.disconnect(callback)

    def trigger(self, *args: P.args):
        self._signal.emit(*args)


class InputContext:

    def __init__(self, key: str):
        self.key = key
        self._actions: Dict[str, InputAction] = {}
        self._frozen = False

    def register(self, action: InputAction[P]) -> InputAction[P]:

        if self._frozen:
            raise RegistryException(f"No further input actions allowed to be registered! ")

        if self.contains(action):
            raise RegistryException(f"Action '{action.key}' already registered in context '{self.key}'")

        self._actions[action.key] = action
        return action

    def get_all(self) -> Set[InputAction]:
        return set(self._actions.values())

    def contains(self, action: InputAction) -> bool:
        return action.key in self._actions

    def freeze(self):
        self._frozen = True

    def is_frozen(self) -> bool:
        return self._frozen


class InputContexts:
    DEFAULT = InputContext("default")
    GENERAL = InputContext("general")
    GAMEPLAY = InputContext("gameplay")
    MENU = InputContext("menus")


class InputActions:

    TOGGLE_PAUSE = InputContexts.GENERAL.register(InputAction[[]]("toggle_pause"))

    PLAYER_MOVE = InputContexts.GENERAL.register(InputAction[Vector2]("player_move"))
    PLAYER_INTERACT = InputContexts.GENERAL.register(InputAction[[]]("player_interact"))
    PLAYER_ATTACK = InputContexts.GENERAL.register(InputAction[[]]("player_attack"))

    MENU_MOVE = InputContexts.GENERAL.register(InputAction[[Vector2]]("menu_move"))
    MENU_SELECT = InputContexts.GENERAL.register(InputAction[[]]("menu_select"))
    MENU_BACK = InputContexts.GENERAL.register(InputAction[[]]("menu_back"))


class InputService:

    def __init__(self):
        self._context_registry = TypeRegistry[InputContext]("core")
        self._active_inputs: Set[int] = set()

    def init(self):
        self._register_contexts()
        self._freeze_contexts()

    def _register_contexts(self):
        for context in vars(InputContexts).values():
            if isinstance(context, InputContext):
                self._context_registry.register(context.key, context)

    def _freeze_contexts(self):
        for context in self.registered_contexts():
            context.freeze()

    def registered_contexts(self) -> Set[InputContext]:
        return set(self._context_registry.get_all().values())

    def register_input(self, input_: int):
        self._active_inputs.add(input_)
        self._on_inputs_updated()

    def remove_input(self, input_: int):
        self._active_inputs.discard(input_)
        self._on_inputs_updated()

    def _on_inputs_updated(self):
        pass