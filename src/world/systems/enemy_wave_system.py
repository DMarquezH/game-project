from enum import Enum, auto
from typing import Dict

from src.entities.enemy_entity import EnemyEntity
from src.services.event_service import EventBus
from src.world.systems.base_system import BaseSystem


class EnemyClass(Enum):
    WEAK = auto()
    STRONG = auto()
    MINIBOSS = auto()
    BOSS = auto()


class EnemyWaveSystem(BaseSystem):

    def __init__(self, event_bus: EventBus):
        super().__init__(event_bus)

        self.enemy_set: Dict[EnemyEntity, EnemyClass] = {}

        self.current_wave = 0