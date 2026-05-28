from typing import List

from pyglet.math import Vec2

from entities.item_entity import ItemEntity
from services.event_service import BaseEvent
from world.systems.shop_system import ShopInstance


class EntityAttackedMeleeEvent(BaseEvent):

    def __init__(self, attacker, attacker_pos: Vec2, attack_dir: Vec2, attack_range: float, amplitude: float, damage: float, knockback: float = 0.0, life_time: float = 0.2):
        super().__init__()
        self.attacker = attacker
        self.attacker_pos = attacker_pos
        self.attack_dir = attack_dir
        self.attack_range = attack_range
        self.amplitude = amplitude
        self.damage = damage
        self.knockback = knockback
        self.life_time = life_time

class EntityAttackedRangedEvent(BaseEvent):

    def __init__(self, attacker, attacker_pos: Vec2, attacker_velocity: Vec2, attack_dir: Vec2, damage: float, knockback: float, speed: float):
        super().__init__()
        self.attacker = attacker
        self.attacker_pos = attacker_pos
        self.attacker_velocity = attacker_velocity
        self.attack_dir = attack_dir
        self.damage = damage
        self.knockback = knockback
        self.speed = speed

class EntityDeadEvent(BaseEvent):
    def __init__(self, entity):
        super().__init__()
        self.entity = entity


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

class CoinCollectedEvent(BaseEvent):
    def __init__(self, amount: int = 1):
        super().__init__()
        self.amount = amount