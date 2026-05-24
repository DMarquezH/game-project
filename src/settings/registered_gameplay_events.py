from typing import List

from pyglet.math import Vec2

from entities.item_entity import ItemEntity
from services.event_service import BaseEvent
from world.systems.shop_system import ShopInstance


class PlayerAttackedMeleeEvent(BaseEvent):

    def __init__(self, player_pos: Vec2, attack_dir: Vec2, attack_range: float, amplitude: float, damage: float):
        super().__init__()

        self.player_pos = player_pos
        self.attack_dir = attack_dir
        self.attack_range = attack_range
        self.amplitude = amplitude
        self.damage = damage


class ToggleShopEvent(BaseEvent):

    def __init__(self, shop):
        super().__init__()
        self.shop = shop


class RerollShopEvent(BaseEvent):

    def __init__(self, shop: ShopInstance):
        super().__init__()
        self.shop = shop

class BuyItemEvent(BaseEvent):

    def __init__(self, item: ItemEntity, shop:ShopInstance):
        super().__init__()
        self.shop = shop
        self.item = item