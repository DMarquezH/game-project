from services.event_service import EventBus
from settings.registered_gameplay_events import PlayerAttackedMeleeEvent
from world.systems.base_system import BaseSystem


class CombatSystem(BaseSystem):

    def __init__(self, event_bus: EventBus):
        super().__init__(event_bus)

    def init(self):

        if self._initialized: return

        self.event_bus.subscribe(PlayerAttackedMeleeEvent, self.on_player_attacked_melee)

        self._initialized = True

    def on_player_attacked_melee(self, event: PlayerAttackedMeleeEvent):

        attack_pos = event.player_pos + event.attack_range * event.attack_dir
        print(f"Attack Pos: {event.attack_dir}")

    def dispose(self):
        self.event_bus.unsubscribe(PlayerAttackedMeleeEvent, self.on_player_attacked_melee)