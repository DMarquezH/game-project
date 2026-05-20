from enum import Enum, auto
from typing import Dict


class StatDefinition(Enum):

    MAX_HEALTH = "max_health"
    HEALTH = "health"

    DEFENSE = "defense"
    ARMOR = "armor"

    MOVEMENT_SPEED = "movement_speed"

    ATTACK_DAMAGE = "attack_damage"
    ATTACK_SPEED = "attack_speed"
    ATTACK_KNOCKBACK = "attack_knockback"

    CRIT_CHANCE = "crit_chance"
    CRIT_DAMAGE_MULTI = "crit_damage_multi"

    ATTACK_RANGE = "attack_range"
    SWING_AMPLITUDE = "swing_amplitude"

    SHOT_SPEED = "shot_speed"
    SHOT_SPREAD = "shot_spread"
    SHOT_PIERCE = "shot_pierce"


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

    @staticmethod
    def resolve(stat:str) -> StatDefinition | None:
        for stat_enum in StatDefinition:
            if stat_enum.value == stat: return stat_enum
        return None