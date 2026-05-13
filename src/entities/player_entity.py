from arcade import Texture

from src.entities.base_entity import BaseEntity
from src.services.event_service import EventBus
from src.settings.registered_gameplay_events import PlayerAttackedMeleeEvent
from src.services.input.settings.registered_input_events import PlayerAttackInputEvent, PlayerMoveInputEvent
from src.world.systems.combat.entity_stats import StatDefinition
from src.world.systems.movement.movement_events import EntityMoveEvent


class Player(BaseEntity):

    DEFAULT_MOVEMENT_SPEED = 5

    DEFAULT_MELEE_RANGE = 20
    DEFAULT_MELEE_AMPLITUDE = 135
    DEFAULT_MELEE_DAMAGE = 35

    def __init__(self, event_bus: EventBus, texture: Texture, scale: float):
        super().__init__(event_bus)

        self.texture = texture
        self.scale = scale

        self.melee_range = Player.DEFAULT_MELEE_RANGE

        # self.stats = EntityStats()

        self._init_stats()
        self._subscribe_events()

    def _init_stats(self):
        self.stats.set(StatDefinition.MOVEMENT_SPEED, self.DEFAULT_MOVEMENT_SPEED)

    def _subscribe_events(self):
        self.event_bus.subscribe(PlayerMoveInputEvent, self._move)
        self.event_bus.subscribe(PlayerAttackInputEvent, self._attack_melee)

    def _unsubscribe_events(self):
        self.event_bus.unsubscribe(PlayerMoveInputEvent, self._move)
        self.event_bus.unsubscribe(PlayerAttackInputEvent, self._attack_melee)

    def _move(self, event: PlayerMoveInputEvent):

        move_dir = event.move_dir.normalize()

        self.event_bus.dispatch(
            EntityMoveEvent(
                self,
                move_dir
            )
        )

    def _attack_melee(self, event: PlayerAttackInputEvent):

        attack_direction = (event.mouse_pos - self.position).normalize()

        self.event_bus.dispatch(PlayerAttackedMeleeEvent(
            self.position,
            attack_direction,
            self.melee_range,
            Player.DEFAULT_MELEE_AMPLITUDE,
            Player.DEFAULT_MELEE_DAMAGE
        ))

    def dispose(self):
        self._unsubscribe_events()