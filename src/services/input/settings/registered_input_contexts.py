from src.services.input.input_context import InputContext
from src.services.input.settings.registered_input_bindings import *


class RegisteredInputContexts:

    DEBUG = InputContext("debug")
    GAMEPLAY = InputContext("gameplay")
    PAUSE = InputContext("pause")

    @staticmethod
    def init():

        RegisteredInputContexts.GAMEPLAY.bind(RegisteredInputBindings.PLAYER_MOVE_WASD)
        RegisteredInputContexts.GAMEPLAY.bind(RegisteredInputBindings.PLAYER_MOVE_ARROWS)
        RegisteredInputContexts.GAMEPLAY.bind(RegisteredInputBindings.PLAYER_ATTACK)
        RegisteredInputContexts.GAMEPLAY.bind(RegisteredInputBindings.TOGGLE_PAUSE)

        RegisteredInputContexts.PAUSE.bind(RegisteredInputBindings.TOGGLE_PAUSE)

        RegisteredInputContexts.DEBUG.bind(RegisteredInputBindings.TOGGLE_DEBUG)