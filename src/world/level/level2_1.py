from pathlib import Path

import arcade
from arcade import Rect

from world.level.base_level import BaseLevel
from settings.game_resources import GameResources


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

    @property
    def bounds(self) -> Rect:
        return arcade.LRBT(
            left=0,
            bottom=0,
            right=64 * 25,
            top=64 * 15
        )