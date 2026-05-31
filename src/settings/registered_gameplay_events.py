from typing import List

from pyglet.math import Vec2

from entities.item_entity import ItemEntity
from services.event_service import BaseEvent
from world.systems.shop_system import ShopInstance


class EntityAttackedMeleeEvent(BaseEvent):

    def __init__(self, attacker, attacker_pos: Vec2, attack_dir: Vec2, attack_range: float, amplitude: float, damage: float, knockback: float = 0.0, life_time: float = 0.2, offset_distance: float = None):
        super().__init__()
        self.attacker = attacker
        self.attacker_pos = attacker_pos
        self.attack_dir = attack_dir
        self.attack_range = attack_range
        self.amplitude = amplitude
        self.damage = damage
        self.knockback = knockback
        self.life_time = life_time
        self.offset_distance = offset_distance

class EntityAttackedRangedEvent(BaseEvent):

    def __init__(self, attacker, attacker_pos: Vec2, attacker_velocity: Vec2, attack_dir: Vec2, damage: float, knockback: float, speed: float, pierce: int = 0, max_distance: float = 1500.0):
        super().__init__()
        self.attacker = attacker
        self.attacker_pos = attacker_pos
        self.attacker_velocity = attacker_velocity
        self.attack_dir = attack_dir
        self.damage = damage
        self.knockback = knockback
        self.speed = speed
        self.pierce = pierce
        self.max_distance = max_distance

class EntityDeadEvent(BaseEvent):
    def __init__(self, entity):
        super().__init__()
        self.entity = entity

class EntityDamagedEvent(BaseEvent):
    def __init__(self, entity, damage: float):
        super().__init__()
        self.entity = entity
        self.damage = damage

class EntityFootstepEvent(BaseEvent):
    def __init__(self, entity):
        super().__init__()
        self.entity = entity

class PlayMusicEvent(BaseEvent):
    def __init__(self, track_name: str):
        super().__init__()
        self.track_name = track_name

class UIButtonClickEvent(BaseEvent):
    def __init__(self):
        super().__init__()

class PopupOpenedEvent(BaseEvent):
    def __init__(self):
        super().__init__()

class GameStartedEvent(BaseEvent):
    def __init__(self):
        super().__init__()


class ToggleShopEvent(BaseEvent):

    def __init__(self, shop):
        super().__init__()
        self.shop = shop


class RerollShopEvent(BaseEvent):

    def __init__(self, shop: ShopInstance):
        super().__init__()
        self.shop = shop

class BuyItemEvent(BaseEvent):
    def __init__(self,item:ItemEntity,shop:ShopInstance):
        super().__init__()
        self.item = item
        self.shop = shop

class ItemBoughtSuccessEvent(BaseEvent):
    def __init__(self, item: ItemEntity):
        super().__init__()
        self.item = item

class CoinCollectedEvent(BaseEvent):
    def __init__(self, amount: int = 1):
        super().__init__()
        self.amount = amount

class GameOverEvent(BaseEvent):
    def __init__(self):
        super().__init__()
