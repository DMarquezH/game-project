import arcade
from pyglet.math import Vec2
from settings.game_resources import GameResources
from entities.combat.hitbox import Hitbox

class MeleeSwipeEntity(Hitbox):
    def __init__(self, attacker, start_pos: tuple[float, float], direction: Vec2, attack_range: float, amplitude: float, damage: float, knockback: float, life_time: float):
        base_range = 64.0
        
        dummy_sprite = arcade.SpriteSolidColor(int(base_range), int(base_range), (255, 0, 0, 0))
        texture = dummy_sprite.texture
        super().__init__(attacker, damage, knockback, texture)
        self.alpha = 0
        self.attack_range = attack_range
        self.direction = direction.normalize()
        
        offset_distance = base_range / 2.0
        offset = direction.normalize() * offset_distance
        self.position = (start_pos[0] + offset.x, start_pos[1] + offset.y)
        
        import math
        self.angle = math.degrees(math.atan2(-direction.y, direction.x))
        
        self.scale = attack_range / base_range
        
        self.life_time = life_time
        self.current_time = 0.0

    def on_update(self, delta_time: float = 1/60):
        self.current_time += delta_time
        if self.current_time >= self.life_time:
            self.kill()
