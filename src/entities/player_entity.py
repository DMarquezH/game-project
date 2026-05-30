import arcade
from arcade import Texture, SpriteSheet

from entities.base_entity import BaseEntity
from services.event_service import EventBus
from services.input.settings.registered_input_events import PlayerAttackInputEvent, PlayerMoveInputEvent, PlayerRangedAttackInputEvent
from settings.registered_gameplay_events import EntityAttackedMeleeEvent, EntityAttackedRangedEvent, EntityFootstepEvent
from world.systems.combat.entity_stats import StatDefinition
from world.systems.movement.movement_events import EntityMoveEvent
from pyglet.math import Vec2

class Player(BaseEntity):

    DEFAULT_MOVEMENT_SPEED = 5

    DEFAULT_MELEE_RANGE = 64
    DEFAULT_MELEE_AMPLITUDE = 135
    DEFAULT_MELEE_DAMAGE = 15.0  
    
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
        self._attack_timer = 0.0
        self._init_stats()
        self._subscribe_events()

    def _init_stats(self):
        self.stats.set(StatDefinition.MOVEMENT_SPEED, self.DEFAULT_MOVEMENT_SPEED)
        self.stats.set(StatDefinition.ATTACK_DAMAGE,self.DEFAULT_MELEE_DAMAGE)
        self.stats.set(StatDefinition.ATTACK_SPEED, 3.0) # 3 ataques por segundo por defecto
        self.stats.set(StatDefinition.SHOT_SPEED, 5.0) # Velocidad del proyectil
        self.stats.set(StatDefinition.MAX_HEALTH, 100.0)
        self.stats.set(StatDefinition.HEALTH, 100.0)
        self.stats.set(StatDefinition.ATTACK_KNOCKBACK, 64.0)
        self.stats.set(StatDefinition.ATTACK_RANGE, Player.DEFAULT_MELEE_RANGE)
        self.stats.set(StatDefinition.SWING_AMPLITUDE, Player.DEFAULT_MELEE_AMPLITUDE)
        self.stats.set(StatDefinition.DEFENSE, 0.0)
        self.stats.set(StatDefinition.ARMOR, 0.0)
        self.stats.set(StatDefinition.CRIT_CHANCE, 0.0)
        self.stats.set(StatDefinition.CRIT_DAMAGE_MULTI, 1.5)
        self.stats.set(StatDefinition.SHOT_PIERCE, 0.0)
        self.stats.set(StatDefinition.SHOT_SPREAD, 0.0)

    def _subscribe_events(self):
        self.event_bus.subscribe(PlayerMoveInputEvent, self._move)
        self.event_bus.subscribe(PlayerAttackInputEvent, self._attack_melee)
        self.event_bus.subscribe(PlayerRangedAttackInputEvent, self._attack_ranged)

    def _unsubscribe_events(self):
        self.event_bus.unsubscribe(PlayerMoveInputEvent, self._move)
        self.event_bus.unsubscribe(PlayerAttackInputEvent, self._attack_melee)
        self.event_bus.unsubscribe(PlayerRangedAttackInputEvent, self._attack_ranged)

    def _move(self, event: PlayerMoveInputEvent):
        # Stun: no nos movemos voluntariamente si acabamos de recibir un buen golpe
        if getattr(self, "invulnerable_timer", 0.0) > 0.3:
            return

        move_dir = event.move_dir.normalize()

        self.event_bus.dispatch(
            EntityMoveEvent(
                self,
                move_dir
            )
        )

    def _attack_melee(self, event: PlayerAttackInputEvent):
        if self._attack_timer > 0:
            return

        attack_speed = self.stats.get(StatDefinition.ATTACK_SPEED) or 3.0
        self._attack_timer = 1.0 / attack_speed
        
        p_pos = Vec2(self.position[0], self.position[1])
        attack_direction = (event.mouse_pos - p_pos).normalize()
        damage = self.stats.get(StatDefinition.ATTACK_DAMAGE) or Player.DEFAULT_MELEE_DAMAGE

        attack_range = self.stats.get(StatDefinition.ATTACK_RANGE) or Player.DEFAULT_MELEE_RANGE
        amplitude = self.stats.get(StatDefinition.SWING_AMPLITUDE) or Player.DEFAULT_MELEE_AMPLITUDE
        knockback = self.stats.get(StatDefinition.ATTACK_KNOCKBACK) or 64.0

        self.event_bus.dispatch(EntityAttackedMeleeEvent(
            attacker=self,
            attacker_pos=self.position,
            attack_dir=attack_direction,
            attack_range=attack_range,
            amplitude=amplitude,
            damage=damage,
            knockback=knockback,
            life_time=(1.0 / attack_speed) * 0.8
        ))

    def _attack_ranged(self, event: PlayerRangedAttackInputEvent):
        if self._attack_timer > 0:
            return

        attack_speed = self.stats.get(StatDefinition.ATTACK_SPEED) or 3.0
        self._attack_timer = 1.0 / attack_speed
        
        p_pos = Vec2(self.position[0], self.position[1])
        attack_direction = (event.mouse_pos - p_pos).normalize()
        damage = self.stats.get(StatDefinition.ATTACK_DAMAGE) or Player.DEFAULT_MELEE_DAMAGE

        shot_speed = self.stats.get(StatDefinition.SHOT_SPEED) or 5.0
        knockback = self.stats.get(StatDefinition.ATTACK_KNOCKBACK) or 64.0
        pierce = int(self.stats.get(StatDefinition.SHOT_PIERCE) or 0)
        attack_range = self.stats.get(StatDefinition.ATTACK_RANGE) or Player.DEFAULT_MELEE_RANGE

        self.event_bus.dispatch(EntityAttackedRangedEvent(
            attacker=self,
            attacker_pos=self.position,
            attacker_velocity=Vec2(self.change_x, self.change_y),
            attack_dir=attack_direction,
            damage=damage,
            knockback=knockback,
            speed=shot_speed,
            pierce=pierce,
            max_distance=attack_range * 6.0
        ))

    def dispose(self):
        self._unsubscribe_events()

    def update_animation(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        if self._attack_timer > 0:
            self._attack_timer -= delta_time
            
        self.update_invulnerability(delta_time)
        self.hurtbox.sync_position()

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
                
                old_frame = self.moving_frame
                self.moving_frame = (self.moving_frame + 1) % len(current_frames)
                
                # Dispatch footstep event on specific frames (e.g. 0 and 2 for a 4-frame walk cycle)
                if self.moving_frame != old_frame and self.moving_frame in [0, 2]:
                    self.event_bus.dispatch(EntityFootstepEvent(self))

            self.texture = self.textures[current_frames[self.moving_frame]]

        else:
            self.anim_time = 0
            self.moving_frame = 0

            self.texture = self.textures[self.static_frame]