import arcade
import random
from pyglet.math import Vec2

from services.event_service import EventBus
from entities.player_entity import Player
from entities.enemies.base_enemy import BaseEnemy
from settings.game_resources import GameResources
from world.systems.combat.entity_stats import StatDefinition
from settings.registered_gameplay_events import EntityAttackedRangedEvent


class RangedEnemy(BaseEnemy):

    def __init__(self, event_bus: EventBus, player: Player, barrier_list=None):
        super().__init__(event_bus, player, barrier_list)
        self._shoot_timer = 0.0
        self._los_timer = 0.0
        self._has_los = False

    def _setup_stats(self) -> None:
        health = random.uniform(20.0, 40.0)
        damage = random.uniform(6.0, 12.0)
        speed = random.uniform(1.2, 1.8)
        
        self.stats.set(StatDefinition.MOVEMENT_SPEED, speed)
        self.stats.set(StatDefinition.MAX_HEALTH,     health)
        self.stats.set(StatDefinition.HEALTH,         health)
        self.stats.set(StatDefinition.ATTACK_DAMAGE,  damage)
        self.stats.set(StatDefinition.ATTACK_SPEED,   1.0) # 1 ataque por segundo
        self.stats.set(StatDefinition.ATTACK_RANGE,   250.0)
        self.stats.set(StatDefinition.SHOT_SPEED, 5.0)
        self.stats.set(StatDefinition.SHOT_SPREAD, 0.0)
        self.stats.set(StatDefinition.ATTACK_KNOCKBACK, 64.0)

    def _setup_texture(self) -> None:
        sheet = arcade.load_spritesheet(GameResources.get("textures") / "entity" / "enemy_spritesheet.png")
        self.textures = sheet.get_texture_grid((209, 270), 6, 16)
        self.texture = self.textures[0]

    def _setup_animation(self) -> None:
        self.walk_down = [0, 1, 2, 3]
        self.walk_up = [4, 5, 6, 7]
        self.walk_right = [8, 9, 10, 11]
        self.walk_left = [12, 13, 14, 15]

    def update_animation(self, delta_time: float) -> None:
        moving = abs(self.change_x) > 0.1 or abs(self.change_y) > 0.1
        if moving:
            if abs(self.change_x) > abs(self.change_y):
                if self.change_x > 0:
                    current_frames = self.walk_right
                else:
                    current_frames = self.walk_left
            else:
                if self.change_y > 0:
                    current_frames = self.walk_up
                else:
                    current_frames = self.walk_down

            self.anim_time += delta_time

            while self.anim_time >= self.anim_fps:
                self.anim_time -= self.anim_fps
                self.frame_index = (self.frame_index + 1) % len(current_frames)

            self.texture = self.textures[current_frames[self.frame_index]]

        else:
            self.anim_time = 0
            self.frame_index = 0
            self.texture = self.textures[self.frame_index]
        
    def _follow_path(self) -> None:
        if getattr(self, "invulnerable_timer", 0.0) > 0.3:
            return

        dist = self._get_distance_to_player()
        attack_range = self.stats.get(StatDefinition.ATTACK_RANGE) or 250.0
        flee_range = 100.0

        if dist < flee_range:
            # Si el jugador está muy cerca, HUIMOS (Kiting)
            dx = self.center_x - self._player.center_x
            dy = self.center_y - self._player.center_y
            direction = Vec2(dx, dy)
            if direction.length() > 0:
                from world.systems.movement.movement_events import EntityMoveEvent
                self.event_bus.dispatch(EntityMoveEvent(self, direction.normalize()))
        
        elif dist > attack_range or not self._has_los:
            super()._follow_path()
        else:
            self._stop()

    def update_behavior(self, delta_time: float) -> None:
        self._los_timer -= delta_time
        if self._los_timer <= 0:
            self._los_timer = 0.25
            if not self._barrier_list or not getattr(self._barrier_list, "blocking_sprites", None):
                self._has_los = True
            else:
                self._has_los = arcade.has_line_of_sight(self.position, self._player.position, self._barrier_list.blocking_sprites, 300)

        dist = self._get_distance_to_player()
        attack_range = self.stats.get(StatDefinition.ATTACK_RANGE) or 250.0
        flee_range = 100.0

        if flee_range <= dist <= attack_range and self._has_los:
            self._try_shoot(delta_time)

    def _try_shoot(self, delta_time: float) -> None:
        self._shoot_timer += delta_time
        attack_speed = self.stats.get(StatDefinition.ATTACK_SPEED)

        if self._shoot_timer >= 1.0 / attack_speed:
            self._shoot_timer = 0.0
            self._shoot()

    def _shoot(self) -> None:
        p_pos = Vec2(self._player.position[0], self._player.position[1])
        m_pos = Vec2(self.position[0], self.position[1])
        direction = (p_pos - m_pos).normalize()
        damage = self.stats.get(StatDefinition.ATTACK_DAMAGE)
        knockback = self.stats.get(StatDefinition.ATTACK_KNOCKBACK)
        shot_speed = self.stats.get(StatDefinition.SHOT_SPEED)
        
        self.event_bus.dispatch(
            EntityAttackedRangedEvent(
                attacker=self,
                attacker_pos=self.position,
                attacker_velocity=Vec2(self.change_x, self.change_y),
                attack_dir=direction,
                damage=damage,
                knockback=knockback,
                speed=shot_speed
            )
        )