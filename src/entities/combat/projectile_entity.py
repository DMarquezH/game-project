import arcade
from pyglet.math import Vec2

from entities.player_entity import Player
from settings.game_resources import GameResources
import math
from entities.combat.hitbox import Hitbox

class ProjectileEntity(Hitbox):
    def __init__(self, attacker, start_pos: tuple[float, float], attacker_velocity: Vec2, direction: Vec2, speed: float, damage: float, knockback: float, pierce: int = 0, max_distance: float = 1500.0):
        if isinstance(attacker, Player):
            texture = arcade.load_texture(GameResources.get("textures") / "effects" / "bullet.png")
        else:
            texture = arcade.load_texture(GameResources.get("textures") / "effects" / "bone.png")
        texture.size = (texture.size[0]/25,texture.size[1]/25)
        super().__init__(attacker, damage, knockback, texture)
        self.position = start_pos
        self.direction = direction.normalize()
        self.speed = speed
        self.max_pierce = pierce
        self.pierce_count = 0
        
        # Calculamos cuánto del movimiento del atacante va en la dirección del disparo
        dot_product = (attacker_velocity.x * self.direction.x) + (attacker_velocity.y * self.direction.y)
        
        # Aumentamos la velocidad general un poco como pidio el usuario (x1.5)
        base_speed = speed * 1.5
        
        # Aplicamos la inercia a la velocidad base. 
        # Ponemos el tope en base_speed * 0.8 para los tiros hacia atrás.
        # Añadimos solo la mitad de inercia (0.4) para los tiros hacia adelante.
        final_speed = max(base_speed * 0.8, base_speed + (dot_product * 0.4))
        
        # La velocidad se aplica estrictamente en línea recta hacia donde se apuntó
        self.velocity_vec = self.direction * final_speed
        

        self.angle = math.degrees(math.atan2(-self.velocity_vec.y, self.velocity_vec.x))
        
        self.max_distance = max_distance
        self.distance_traveled = 0.0

    def on_update(self, delta_time: float = 1/60):
        dt_scale = delta_time * 60
        scaled_velocity = self.velocity_vec * dt_scale
        move_step = scaled_velocity.length()
        
        self.center_x += scaled_velocity.x
        self.center_y += scaled_velocity.y
        self.distance_traveled += move_step
        
        if self.distance_traveled >= self.max_distance:
            self.kill()
