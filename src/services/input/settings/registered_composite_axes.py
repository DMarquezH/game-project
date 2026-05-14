import arcade

from services.input.devices.keyboard_device import KeyboardInputDevice
from services.input.util.composite_axis import CompositeAxis


class RegisteredCompositeAxes:

    WASD = CompositeAxis(

        up=KeyboardInputDevice.signature_from_key(
            arcade.key.W
        ),
        down=KeyboardInputDevice.signature_from_key(
            arcade.key.S
        ),
        left=KeyboardInputDevice.signature_from_key(
            arcade.key.A
        ),
        right=KeyboardInputDevice.signature_from_key(
            arcade.key.D
        )
    )

    ARROW_KEYS = CompositeAxis(

        up=KeyboardInputDevice.signature_from_key(
            arcade.key.UP
        ),
        down=KeyboardInputDevice.signature_from_key(
            arcade.key.DOWN
        ),
        left=KeyboardInputDevice.signature_from_key(
            arcade.key.LEFT
        ),
        right=KeyboardInputDevice.signature_from_key(
            arcade.key.RIGHT
        )
    )