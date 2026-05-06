import arcade
from pyglet.math import Vec2


class MeleeAttack(arcade.Sprite):

    def __init__(self, position: Vec2, direction: Vec2, amplitude: float, damage: float):
        super().__init__()
        self.position = position
        self.direction = direction
        self.amplitude = amplitude
        self.damage = damage
