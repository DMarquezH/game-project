from pyglet.math import Vec2

from src.core.event.event_service import BaseEvent


class PlayerAttackedMeleeEvent(BaseEvent):

    def __init__(self, player_pos: Vec2, attack_dir: Vec2, attack_range: float, amplitude: float, damage: float):
        super().__init__()

        self.player_pos = player_pos
        self.attack_dir = attack_dir
        self.attack_range = attack_range
        self.amplitude = amplitude
        self.damage = damage