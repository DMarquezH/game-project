from enum import Enum, auto
from typing import Dict


class StatDefinition(Enum):

    MAX_HEALTH = auto()
    HEALTH = auto()

    DEFENSE = auto()
    ARMOR = auto()

    MOVEMENT_SPEED = auto()

    ATTACK_DAMAGE = auto()
    ATTACK_SPEED = auto()
    ATTACK_KNOCKBACK = auto()

    CRIT_CHANCE = auto()
    CRIT_DAMAGE_MULTI = auto()

    ATTACK_RANGE = auto()
    SWING_AMPLITUDE = auto()

    SHOT_SPEED = auto()
    SHOT_SPREAD = auto()
    SHOT_PIERCE = auto()


class EntityStats:

    def __init__(self):
        self.values: Dict[StatDefinition, float] = {}

    def get(self, stat_def: StatDefinition) -> float | None:
        return self.values.get(stat_def)

    def set(self, stat_def: StatDefinition, value: float):
        self.values[stat_def] = value

    def increase(self, stat_def: StatDefinition, increase: float):

        stat_value = self.get(stat_def)
        if not stat_value: return

        self.set(stat_def, stat_value + increase)

    def decrease(self, stat_def: StatDefinition, decrease: float):

        stat_value = self.get(stat_def)
        if not stat_value: return

        self.set(stat_def, stat_value - decrease)