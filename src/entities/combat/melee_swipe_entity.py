import arcade
from pyglet.math import Vec2
from settings.game_resources import GameResources
from entities.combat.hitbox import Hitbox

class MeleeSwipeEntity(Hitbox):
    def __init__(self, attacker, start_pos: tuple[float, float], direction: Vec2, attack_range: float, amplitude: float, damage: float, knockback: float, life_time: float, offset_distance: float = None):
        dummy_sprite = arcade.SpriteSolidColor(int(attack_range), int(amplitude), (255, 0, 0, 0))
        texture = dummy_sprite.texture
        super().__init__(attacker, damage, knockback, texture)
        self.alpha = 0
        self.attack_range = attack_range
        self.amplitude = amplitude
        self.direction = direction.normalize()
        
        if offset_distance is None:
            offset_distance = attack_range / 2.0
            
        offset = direction.normalize() * offset_distance
        self.position = (start_pos[0] + offset.x, start_pos[1] + offset.y)
        
        import math
        self.angle = math.degrees(math.atan2(-direction.y, direction.x))
        
        self.scale = 1.0
        
        self.life_time = life_time
        self.current_time = 0.0

    def on_update(self, delta_time: float = 1/60):
        self.current_time += delta_time
        if self.current_time >= self.life_time:
            self.kill()
