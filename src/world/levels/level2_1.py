from pathlib import Path
from src.world.levels.base_level import BaseLevel
from src.settings.game_resources import GameResources


class Level2_1(BaseLevel):

    @property
    def tilemap_path(self) -> Path:
        return GameResources.get("levels") / "level_2" / "LV2_1.0.tmj"

    @property
    def layer_options(self) -> dict[str, dict]:
        return {
            "Top2":      {"use_spatial_hash": True},
            "top1":      {"use_spatial_hash": True},
            "Border":    {"use_spatial_hash": True},
            "Border2":   {"use_spatial_hash": True},
            "Obstacles": {"use_spatial_hash": True},
        }

    @property
    def collision_layers(self) -> list[str]:
        return ["Obstacles", "Border", "Border2"]
