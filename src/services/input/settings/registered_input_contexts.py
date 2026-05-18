from services.input.input_context import InputContext
from services.input.settings.registered_input_bindings import *


class RegisteredInputContexts:

    GENERAL = InputContext("general")
    DEBUG = InputContext("debug")
    GAMEPLAY = InputContext("gameplay")
    PAUSE = InputContext("pause")

    @staticmethod
    def init():

        RegisteredInputContexts.GENERAL.bind(RegisteredInputBindings.TOGGLE_FULLSCREEN)

        RegisteredInputContexts.GAMEPLAY.bind(RegisteredInputBindings.PLAYER_MOVE_WASD)
        RegisteredInputContexts.GAMEPLAY.bind(RegisteredInputBindings.PLAYER_MOVE_ARROWS)
        RegisteredInputContexts.GAMEPLAY.bind(RegisteredInputBindings.PLAYER_ATTACK)
        RegisteredInputContexts.GAMEPLAY.bind(RegisteredInputBindings.TOGGLE_PAUSE)

        RegisteredInputContexts.PAUSE.bind(RegisteredInputBindings.TOGGLE_PAUSE)

        RegisteredInputContexts.DEBUG.bind(RegisteredInputBindings.TOGGLE_DEBUG)