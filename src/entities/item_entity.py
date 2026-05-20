from pathlib import Path

import arcade

from settings.game_resources import GameResources


class ItemEntity():
    def __init__(self,texture:Path, name: str,description:str,cost:float,value:float,stat:str):

        self.texture = arcade.load_texture(GameResources.get("textures") / texture)
        self.name: str = name
        self.description: str = description
        self.cost: float = cost
        self.value: float = value
        self.stat: str = stat

    def __eq__(self, other):
        return self.name == other.name