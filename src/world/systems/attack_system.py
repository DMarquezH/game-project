from src.core.event.event_service import EventBus
from src.core.event.game_events import PlayerAttackedMeleeEvent


class AttackSystem:

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.initialized = False

    def _init(self):

        if self.initialized: return

        # Suscripciones a eventos
        self.event_bus.subscribe(PlayerAttackedMeleeEvent, self.on_player_attacked_melee)

        self.initialized = True

    def on_player_attacked_melee(self, event: PlayerAttackedMeleeEvent):
        pass