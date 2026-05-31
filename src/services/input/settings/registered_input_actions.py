from services.event_service import EventBus
from services.input.input_action import InputAction, T
from services.input.input_type import AxisInput, EmptyInput
from services.input.settings.registered_input_events import *





class PlayerMoveInputAction(InputAction):

    def activate(self, event_bus: EventBus, input_value: AxisInput):

        event_bus.dispatch(
            PlayerMoveInputEvent(
                Vec2(input_value.x, input_value.y)
            )
        )


class PlayerAttackInputAction(InputAction):

    def activate(self, event_bus: EventBus, input_value: AxisInput):

        event_bus.dispatch(
            PlayerAttackInputEvent(
                Vec2(input_value.x, input_value.y)
            )
        )

class PlayerRangedAttackInputAction(InputAction):

    def activate(self, event_bus: EventBus, input_value: AxisInput):

        event_bus.dispatch(
            PlayerRangedAttackInputEvent(
                Vec2(input_value.x, input_value.y)
            )
        )


class TogglePauseInputAction(InputAction):

    def activate(self, event_bus: EventBus, input_value: EmptyInput):
        event_bus.dispatch(TogglePauseInputEvent())


class ToggleDebugInputAction(InputAction):

    def activate(self, event_bus: EventBus, input_value: EmptyInput):
        event_bus.dispatch(ToggleDebugInputEvent())
