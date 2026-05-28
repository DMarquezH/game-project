import arcade
from pyglet.math import Vec2
from settings.game_resources import GameResources

class MeleeSwipeEntity(arcade.Sprite):
    def __init__(self, attacker, start_pos: tuple[float, float], direction: Vec2, attack_range: float, amplitude: float, damage: float, knockback: float, life_time: float):
        texture = arcade.load_texture(GameResources.get("textures") / "effects" / "swipe_64.png")
        super().__init__(texture)
        self.attacker = attacker
        self.damage = damage
        self.knockback = knockback
        self.attack_range = attack_range
        self.direction = direction.normalize()
        
        # Desplazar el swipe hacia adelante
        offset_distance = attack_range * 0.5
        offset = direction.normalize() * offset_distance
        self.position = (start_pos[0] + offset.x, start_pos[1] + offset.y)
        
        import math
        self.angle = math.degrees(math.atan2(-direction.y, direction.x))
        
        # Hacerlo de tamaño normal
        self.scale = 1.0
        
        self.life_time = life_time
        self.current_time = 0.0
        
        # Track hit entities to not hit them multiple times in one swing
        self.hit_entities = set()

    def on_update(self, delta_time: float = 1/60):
        self.current_time += delta_time
        if self.current_time >= self.life_time:
            self.kill()
