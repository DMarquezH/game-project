import arcade
import random

from pyglet.math import Vec2
from services.event_service import EventBus
from entities.player_entity import Player
from entities.enemies.base_enemy import BaseEnemy
from settings.game_resources import GameResources
from world.systems.combat.entity_stats import StatDefinition
from settings.registered_gameplay_events import EntityAttackedMeleeEvent


class FastEnemy(BaseEnemy):

    ATTACK_DISTANCE = 25.0 

    def __init__(self, event_bus: EventBus, player: Player, barrier_list=None):
        super().__init__(event_bus, player, barrier_list)
        self._attack_timer = 0.0
        self.event_bus.subscribe(EntityAttackedMeleeEvent, self.attack_animation)
        # chikIbai
        self.scale = 0.2
        self.anim_fps = 1/15

    def _setup_stats(self) -> None:
        # Randomizamos levemente las estadisticas base
        health = random.uniform(35.0, 50.0)
        damage = random.uniform(10.0, 15.0)
        speed = random.uniform(4.0, 5.0)
        
        self.stats.set(StatDefinition.MOVEMENT_SPEED, speed)
        self.stats.set(StatDefinition.MAX_HEALTH, health)
        self.stats.set(StatDefinition.HEALTH, health)
        self.stats.set(StatDefinition.ATTACK_DAMAGE, damage)
        self.stats.set(StatDefinition.ATTACK_SPEED, 3.0)
        self.stats.set(StatDefinition.ATTACK_KNOCKBACK, 32.0)

    def _setup_texture(self) -> None:
        sheet = arcade.load_spritesheet(GameResources.get("textures")/ "entity" / "enemy_spritesheet.png")
        self.textures = sheet.get_texture_grid((209,270),6,24)
        self.texture = self.textures[0]

    def _setup_animation(self) -> None:
        self.walk_down = [0,1,2,3]
        self.walk_up = [4,5,6,7]
        self.walk_right = [8,9,10,11]
        self.walk_left = [12,13,14,15]
        self.attack_left = [18, 19]
        self.attack_right = [20, 21]
        self.attack_up = [22, 23]
        self.attack_down = [16, 17]

    def attack_animation(self, event: EntityAttackedMeleeEvent):
        # Filtro para que solo ataquen los que realmente han atacado
        if event.attacker is not self:
            return

        direction = event.attack_dir

        if abs(direction.x) > abs(direction.y):
            if direction.x > 0:
                self.last_dir = "right"
            else:
                self.last_dir = "left"
        else:
            if direction.y > 0:
                self.last_dir = "up"
            else:
                self.last_dir = "down"

        self.anim_state = "attack"
        self.frame_index = 0
        self.anim_time = 0.0

    def update_behavior(self, delta_time: float) -> None:
        if self._get_distance_to_player() <= self.ATTACK_DISTANCE:
            self._stop()
            self._try_attack(delta_time)
        else:
            pass # BaseEnemy ya maneja el movimiento y por eso se bugueaban en las piedras


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