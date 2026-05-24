import arcade
from arcade import Texture, SpriteSheet

from entities.base_entity import BaseEntity
from services.event_service import EventBus
from settings.registered_gameplay_events import PlayerAttackedMeleeEvent
from services.input.settings.registered_input_events import PlayerAttackInputEvent, PlayerMoveInputEvent
from world.systems.combat.entity_stats import StatDefinition
from world.systems.movement.movement_events import EntityMoveEvent


class Player(BaseEntity):

    DEFAULT_MOVEMENT_SPEED = 5

    DEFAULT_MELEE_RANGE = 20
    DEFAULT_MELEE_AMPLITUDE = 135
    DEFAULT_MELEE_DAMAGE = 35

    def __init__(self, event_bus: EventBus, sheet: SpriteSheet, scale: float):
        super().__init__(event_bus)

        self.scale = scale

        self.melee_range = Player.DEFAULT_MELEE_RANGE


        self.sprite_sheet= sheet
        self.textures: list[Texture] = self.sprite_sheet.get_texture_grid((209,270),6,17)


        #Definicion de texturas
        self.left_frames = [12,13,14,15]
        self.right_frames = [8,9,10,11]
        self.up_frames = [4,5,6,7]
        self.down_frames = [0,1,2,3]
        self.static_frame = 16

        self.anim_time = 0
        self.anim_fps = 1/6
        self.moving_frame = 0

        self.texture = self.textures[self.static_frame]
        self._init_stats()
        self._subscribe_events()

    def _init_stats(self):
        self.stats.set(StatDefinition.MOVEMENT_SPEED, self.DEFAULT_MOVEMENT_SPEED)
        self.stats.set(StatDefinition.ATTACK_DAMAGE,self.DEFAULT_MELEE_DAMAGE)

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

    def update_animation(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        moving = abs(self.change_x) >0.1 or abs(self.change_y) >0.1
        if moving:
            if abs(self.change_x) > abs(self.change_y):
                if self.change_x > 0:
                    current_frames = self.right_frames
                else:
                    current_frames = self.left_frames
            else:
                if self.change_y > 0:
                    current_frames = self.up_frames
                else:
                    current_frames = self.down_frames

            self.anim_time += delta_time

            while self.anim_time >= self.anim_fps:
                self.anim_time -= self.anim_fps
                self.moving_frame = (self.moving_frame + 1) % len(current_frames)

            self.texture = self.textures[current_frames[self.moving_frame]]

        else:
            self.anim_time = 0
            self.moving_frame = 0

            self.texture = self.textures[self.static_frame]