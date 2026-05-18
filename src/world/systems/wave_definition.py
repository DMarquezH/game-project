from dataclasses import dataclass, field
from entities.enemies.base_enemy import BaseEnemy


@dataclass
class EnemySpawnEntry:
    enemy_type: type[BaseEnemy]
    count: int


@dataclass
class WaveDefinition:
    entries: list[EnemySpawnEntry]
    spawn_interval: float = 1.0