import arcade
from arcade import Texture
from pyglet.math import Vec2

from services.event_service import EventBus
from settings.game_events import PlayerAttackedMeleeEvent


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

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        pass

    def move(self, move_dir: Vec2):
        self.change_x = self.movement_speed * self.movement_speed_multi * move_dir.x
        self.change_y = self.movement_speed * self.movement_speed_multi * move_dir.y

    # Falta implementar InputService
    def attack_melee(self, cursor_pos: Vec2):

        attack_direction = (cursor_pos - self.position).normalize()

        # Notificamos el ataque melee del jugador usando el bus de eventos
        self.event_bus.dispatch(PlayerAttackedMeleeEvent(
            self.position,
            attack_direction,
            self.melee_range,
            Player.DEFAULT_MELEE_AMPLITUDE,
            Player.DEFAULT_MELEE_DAMAGE
        ))