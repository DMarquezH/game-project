from pathlib import Path

from arcade.resources import add_resource_handle, resolve


class GameResources:

    _initialized = False

    @classmethod
    def init(cls):

        if cls._initialized:
            return

        assets_path = Path(__file__).parent.parent.parent / "assets"
        add_resource_handle("assets", assets_path)

        add_resource_handle("textures", assets_path / "textures")
        add_resource_handle("sounds", assets_path / "sounds")
        add_resource_handle("levels", assets_path / "levels")
        add_resource_handle("fonts", assets_path / "fonts")
        add_resource_handle("data", assets_path / "data")

        cls._initialized = True

    @staticmethod
    def get(key: str) -> Path:
        return resolve(f":{key}:")