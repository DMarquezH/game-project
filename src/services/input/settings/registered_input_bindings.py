import arcade

from services.input.devices.keyboard_device import KeyboardInputDevice
from services.input.devices.mouse_device import MouseInputDevice
from services.input.input_binding import InputTrigger, CompositeAxisInputBinding, SimpleInputBinding
from services.input.settings.registered_composite_axes import RegisteredCompositeAxes
from services.input.settings.registered_input_actions import *


class RegisteredInputBindings:

    ### GENERAL ###

    TOGGLE_FULLSCREEN = SimpleInputBinding(
        KeyboardInputDevice.signature_from_key(
            arcade.key.F11
        ),
        ToggleFullscreenInputAction(),
        InputTrigger.PRESS
    )

    ### GAMEPLAY ###

    PLAYER_MOVE_WASD = CompositeAxisInputBinding(
        RegisteredCompositeAxes.WASD,
        PlayerMoveInputAction(),
    )

    PLAYER_MOVE_ARROWS = CompositeAxisInputBinding(
        RegisteredCompositeAxes.ARROW_KEYS,
        PlayerMoveInputAction(),
    )

    PLAYER_ATTACK = SimpleInputBinding(
        MouseInputDevice.signature_from_button(
            arcade.MOUSE_BUTTON_LEFT
        ),
        PlayerAttackInputAction(),
        InputTrigger.PRESS
    )

    PLAYER_RANGED_ATTACK = SimpleInputBinding(
        MouseInputDevice.signature_from_button(
            arcade.MOUSE_BUTTON_RIGHT
        ),
        PlayerRangedAttackInputAction(),
        InputTrigger.PRESS
    )

    ### PAUSE ###

    TOGGLE_PAUSE = SimpleInputBinding(
        KeyboardInputDevice.signature_from_key(
            arcade.key.ESCAPE
        ),
        TogglePauseInputAction(),
        InputTrigger.PRESS
    )

    ### DEBUG ###

    TOGGLE_DEBUG = SimpleInputBinding(
        KeyboardInputDevice.signature_from_key(
            arcade.key.F3
        ),
        ToggleDebugInputAction(),
        InputTrigger.PRESS
    )

    ### SHOP TEMP ###

    TOGGLE_SHOP = SimpleInputBinding(
        KeyboardInputDevice.signature_from_key(
            arcade.key.P
        ),
        ToggleShopInputAction(),
        InputTrigger.PRESS
    )