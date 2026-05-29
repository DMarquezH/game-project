import arcade

class Hitbox(arcade.Sprite):
    def __init__(self, attacker, damage: float, knockback: float, texture: arcade.Texture = None):
        if texture:
            super().__init__(texture)
        else:
            super().__init__()
            
        self.attacker = attacker
        self.damage = damage
        self.knockback = knockback
        
        self.hit_entities = set()
