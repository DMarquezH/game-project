from abc import ABC, abstractmethod
from pathlib import Path
from arcade import TileMap
class BaseLevel(ABC):

    @property
    @abstractmethod
    def tilemap_path(self) -> Path: ...

    @property
    @abstractmethod
    def layer_options(self) -> dict[str, dict]: ...

    @property
    @abstractmethod
    def collision_layers(self) -> list[str]: ...


    def player_start(self, tile_map: TileMap) -> tuple[float, float]:
        spawn = tile_map.object_lists["Entities"][0]
        return spawn.shape[0], spawn.shape[1]