import arcade
import random

from pyglet.math import Vec2
from services.event_service import EventBus
from entities.player_entity import Player
from entities.enemies.base_enemy import BaseEnemy
from settings.game_resources import GameResources
from world.systems.combat.entity_stats import StatDefinition
from settings.registered_gameplay_events import EntityAttackedMeleeEvent


class MeleeEnemy(BaseEnemy):

    ATTACK_DISTANCE = 50.0 

    def __init__(self, event_bus: EventBus, player: Player, barrier_list=None):
        super().__init__(event_bus, player, barrier_list)
        self._attack_timer = 0.0

    def _setup_stats(self) -> None:
        # Randomizamos levemente las estadisticas base
        health = random.uniform(40.0, 60.0)
        damage = random.uniform(8.0, 15.0)
        speed = random.uniform(1.8, 2.3)
        
        self.stats.set(StatDefinition.MOVEMENT_SPEED, speed)
        self.stats.set(StatDefinition.MAX_HEALTH, health)
        self.stats.set(StatDefinition.HEALTH, health)
        self.stats.set(StatDefinition.ATTACK_DAMAGE, damage)
        self.stats.set(StatDefinition.ATTACK_SPEED, 1.0) # 1 ataque por segundo
        self.stats.set(StatDefinition.ATTACK_KNOCKBACK, 64.0)

    def _setup_texture(self) -> None:
        sheet = arcade.load_spritesheet(GameResources.get("textures")/ "entity" / "enemy_spritesheet.png")
        self.textures = sheet.get_texture_grid((209,270),6,16)
        self.texture = self.textures[0]

    def _setup_animation(self) -> None:
        self.walk_down = [0,1,2,3]
        self.walk_up = [4,5,6,7]
        self.walk_right = [8,9,10,11]
        self.walk_left = [12,13,14,15]

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

    def update_behavior(self, delta_time: float) -> None:
        if self._get_distance_to_player() <= self.ATTACK_DISTANCE:
            self._stop()
            self._try_attack(delta_time)
        else:
            self._follow_path()

    def _try_attack(self, delta_time: float) -> None:
        self._attack_timer += delta_time
        attack_speed = self.stats.get(StatDefinition.ATTACK_SPEED)

        if self._attack_timer >= 1.0 / attack_speed:
            self._attack_timer = 0.0
            self._attack()

    def _attack(self) -> None:
        p_pos = Vec2(self._player.position[0], self._player.position[1])
        m_pos = Vec2(self.position[0], self.position[1])
        direction = (p_pos - m_pos).normalize()
        damage = self.stats.get(StatDefinition.ATTACK_DAMAGE)
        knockback = self.stats.get(StatDefinition.ATTACK_KNOCKBACK)
        
        self.event_bus.dispatch(EntityAttackedMeleeEvent(
            attacker=self,
            attacker_pos=self.position,
            attack_dir=direction,
            attack_range=self.ATTACK_DISTANCE,
            amplitude=90.0,
            damage=damage,
            knockback=knockback
        ))