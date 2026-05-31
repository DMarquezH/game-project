import arcade
import random
import math
from pyglet.math import Vec2
from entities.combat.hurtbox import Hurtbox
from services.event_service import EventBus
from entities.player_entity import Player
from entities.enemies.base_enemy import BaseEnemy
from settings.game_resources import GameResources
from world.systems.combat.entity_stats import StatDefinition
from settings.registered_gameplay_events import EntityAttackedMeleeEvent
from world.systems.movement.movement_events import EntityMoveEvent


class BossEnemy(BaseEnemy):

    ATTACK_DISTANCE = 130.0 

    def __init__(self, event_bus: EventBus, player: Player, barrier_list=None):
        super().__init__(event_bus, player, barrier_list)
        self._attack_timer = 0.0
        self._hover_time = 0.0
        self.event_bus.subscribe(EntityAttackedMeleeEvent, self.attack_animation)
        self.scale = 1.0
        
        if hasattr(self, "hurtbox") and self.hurtbox:
            self.hurtbox.kill()
        self.hurtbox = Hurtbox(self, width=96, height=192)

    def _setup_stats(self) -> None:
        health = 1200.0
        damage = 40.0
        speed = 1.2
        
        self.stats.set(StatDefinition.MOVEMENT_SPEED, speed)
        self.stats.set(StatDefinition.MAX_HEALTH, health)
        self.stats.set(StatDefinition.HEALTH, health)
        self.stats.set(StatDefinition.ATTACK_DAMAGE, damage)
        self.stats.set(StatDefinition.ATTACK_SPEED, 0.5) 
        self.stats.set(StatDefinition.ATTACK_KNOCKBACK, 64*3)

    def _setup_texture(self) -> None:
        sheet = arcade.load_spritesheet(GameResources.get("textures")/ "entity" / "boss_spritesheet.png")
        self.textures = sheet.get_texture_grid((209,270),7,7)
        self.texture = self.textures[0]
        self.scale = 1.0

        self.color = arcade.color.GHOST_WHITE   # tinte para que se vea distinto de mientras
        self.alpha = 200 # Ligeramente transparente por ser un fantasma

    def _setup_animation(self) -> None:
        self.walk_down = [0]
        self.walk_up = [1]
        self.walk_right = [2]
        self.walk_left = [3]
        self.attack_down = [4,5,6]

    def attack_animation(self, event: EntityAttackedMeleeEvent):
        # Filtro para que solo ataquen los que realmente han atacado
        if event.attacker is not self:
            return

        self.last_dir = "down"

        self.anim_state = "attack"
        self.frame_index = 0
        self.anim_time = 0.0

    def _follow_path(self) -> None:
        # Ignora los muros y el A* pathfinding.
        
        if getattr(self, "invulnerable_timer", 0.0) > 0.3:
            return
            
        dx = self._player.center_x - self.center_x
        dy = self._player.center_y - self.center_y
        direction = Vec2(dx, dy)
        
        if direction.length() > 0:
            direction = direction.normalize()
            # Añadimos el efecto "hover" en el eje Y
            hover_amplitude = 0.5 
            hover_offset = math.sin(self._hover_time * 4.0) * hover_amplitude
            
            direction = Vec2(direction.x, direction.y + hover_offset)
            
            self.event_bus.dispatch(EntityMoveEvent(self, direction))

    def update_behavior(self, delta_time: float) -> None:
        self._hover_time += delta_time
        
        if self._get_distance_to_player() <= self.ATTACK_DISTANCE:
            self._stop()
            self._try_attack(delta_time)
        else:
            # BaseEnemy ya llama a _follow_path(),
            pass

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
            attack_range=256.0,  # Largo del rectángulo 
            amplitude=144.0,     # Ancho del rectángulo 
            damage=damage,
            knockback=knockback,
            offset_distance=0.0  # Centrado en el jefe
        ))
