from src.services.event_service import EventBus
from src.settings.game_events import PlayerAttackedMeleeEvent
from src.world.systems.base_system import BaseSystem


class AttackSystem(BaseSystem):

    def __init__(self, event_bus: EventBus):
        super().__init__(event_bus)

    def init(self):

        if self._initialized: return

        self.event_bus.subscribe(PlayerAttackedMeleeEvent, self.on_player_attacked_melee)

        self._initialized = True

    def on_player_attacked_melee(self, event: PlayerAttackedMeleeEvent):

        attack_pos = event.player_pos + event.attack_range * event.attack_dir
        print(f"Attack Pos: {event.attack_dir}")