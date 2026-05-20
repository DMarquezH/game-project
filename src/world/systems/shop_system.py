from typing import List

from entities.item_entity import ItemEntity
from services.event_service import EventBus



class ShopInstance:

    INIT_REROLL_COST = 0
    REROLL_COST_INCREMENT = 1

    def __init__(self, event_bus: EventBus, items: List[ItemEntity]):
        self.event_bus = event_bus
        self.active_items = items
        self.used_items = []

        self.current_reroll_cost = self.INIT_REROLL_COST
        self.reroll_cost_increment = self.REROLL_COST_INCREMENT

    def reroll(self):
        self.current_reroll_cost += self.reroll_cost_increment
        self.used_items.clear()
        for item in self.active_items:
            self.used_items.append(item)
        self.active_items.clear()
    def load_new_items(self, new_items: List[ItemEntity]):
        self.active_items = new_items
        #self.event_bus.dispatch(RerollShopEvent(self.active_items))