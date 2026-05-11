from typing import Dict, Set

from src.core.service_container import Service
from src.services.event_service import EventBus
from src.services.input.game_input import GameInput, InputSignature
from src.services.input.input_action import InputAction
from src.services.input.input_binding import InputTrigger, InputBinding, ActiveInput
from src.services.input.input_context import InputContext
from src.services.input.input_type import InputType
from src.services.input.util.composite_axis import CompositeAxis


class InputService(Service):

    def __init__(self, event_bus: EventBus):
        super().__init__("input")

        self.event_bus = event_bus

        self.composite_axes: Set[CompositeAxis] = set()

        self.active_contexts: Dict[str, InputContext] = {}
        self.active_inputs: Dict[InputSignature, ActiveInput] = {}

    def update(self):
        self._process_active_inputs()

    def _process_active_inputs(self):

        binding_buffer: Set[InputBinding] = set()
        action_buffer: Dict[InputAction, InputType] = {}

        for signature, active_input in self.active_inputs.items():

            binding = active_input.binding
            if binding in binding_buffer: continue

            value = binding.resolve_value(self.active_inputs.copy())
            action_buffer[binding.input_action] = value

            binding_buffer.add(binding)

        self._activate_actions(action_buffer)

    def enable_context(self, context: InputContext):
        self.active_contexts[context.name] = context
        self._on_contexts_changed()

    def disable_context(self, context: InputContext):
        self.active_contexts.pop(context.name, None)
        self._on_contexts_changed()

    def _on_contexts_changed(self):

        input_buffer: Set[ActiveInput] = set()

        for active_input in self.active_inputs.values():

            binding = active_input.binding

            for context in self.active_contexts.values():

                if binding in context.bindings.values():
                    input_buffer.add(active_input)

        self.active_inputs = {
            s: i
            for s, i in self.active_inputs.items()
            if i in input_buffer
        }

    def register_press(self, game_input: GameInput):
        self._process_input(game_input, InputTrigger.PRESS)

    def register_release(self, game_input: GameInput):
        self._process_input(game_input, InputTrigger.RELEASE)

    def register_change(self, game_input: GameInput):
        self._process_input(game_input, InputTrigger.CHANGE)

    def _process_input(self, game_input: GameInput, trigger: InputTrigger):

        action_buffer: Dict[InputAction, InputType] = {}

        for context in self.active_contexts.values():

            binding = context.bindings.get(game_input.signature)
            if not binding: continue

            if binding.trigger == InputTrigger.HOLD and not trigger == InputTrigger.CHANGE:
                self._process_input_state(game_input, binding, trigger)
                continue

            if not binding.trigger == trigger: continue
            action_buffer[binding.input_action] = game_input.value

        self._activate_actions(action_buffer)

    def _process_input_state(self, game_input: GameInput, binding: InputBinding, trigger: InputTrigger):

        signature = game_input.signature

        if trigger == InputTrigger.PRESS:
            active_input = ActiveInput(signature, binding, game_input.value)
            self.active_inputs[game_input.signature] = active_input

        elif trigger == InputTrigger.RELEASE:
            self.active_inputs.pop(game_input.signature, None)

    def _activate_actions(self, action_buffer: Dict[InputAction, InputType]):

        for action, value in action_buffer.items():
            action.activate(self.event_bus, value)