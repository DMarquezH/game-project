import arcade
from arcade import Texture

from src.services.event_service import EventBus
from src.settings.registered_gameplay_events import PlayerAttackedMeleeEvent
from src.services.input.settings.registered_input_events import PlayerAttackInputEvent, PlayerMoveInputEvent


class Player(arcade.Sprite):

    DEFAULT_MOVEMENT_SPEED = 5
    DEFAULT_MOVEMENT_SPEED_MULTI = 1

    DEFAULT_ATTACK_SPEED = 0.5

    DEFAULT_MELEE_RANGE = 20
    DEFAULT_MELEE_AMPLITUDE = 135
    DEFAULT_MELEE_DAMAGE = 35

    def __init__(self, event_bus: EventBus, texture: Texture, scale: float):
        super().__init__(texture, scale)

        self.event_bus = event_bus

        self.movement_speed = Player.DEFAULT_MOVEMENT_SPEED
        self.movement_speed_multi = Player.DEFAULT_MOVEMENT_SPEED_MULTI

        self.melee_range = Player.DEFAULT_MELEE_RANGE

        # self.stats = EntityStats()

        self.subscribe_events()

    def subscribe_events(self):
        self.event_bus.subscribe(PlayerMoveInputEvent, self.move)
        self.event_bus.subscribe(PlayerAttackInputEvent, self.attack_melee)

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):

        if self.change_x != 0:
            self.change_x = round(self.change_x * 0.8, 2)

        if self.change_y != 0:
            self.change_y = round(self.change_y * 0.8, 2)

    def move(self, event: PlayerMoveInputEvent):

        move_dir = event.move_dir.normalize()

        self.change_x = self.movement_speed * self.movement_speed_multi * move_dir.x
        self.change_y = self.movement_speed * self.movement_speed_multi * move_dir.y

    def attack_melee(self, event: PlayerAttackInputEvent):

        attack_direction = (event.mouse_pos - self.position).normalize()

        self.event_bus.dispatch(PlayerAttackedMeleeEvent(
            self.position,
            attack_direction,
            self.melee_range,
            Player.DEFAULT_MELEE_AMPLITUDE,
            Player.DEFAULT_MELEE_DAMAGE
        ))