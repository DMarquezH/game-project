import arcade
import random
from services.event_service import EventBus
from settings.game_resources import GameResources
from settings.registered_gameplay_events import CoinCollectedEvent, EntityAttackedMeleeEvent, EntityAttackedRangedEvent, EntityDamagedEvent, EntityFootstepEvent, UIButtonClickEvent, PopupOpenedEvent, GameStartedEvent, ItemBoughtSuccessEvent, PlayMusicEvent
from entities.player_entity import Player

class AudioService:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.sounds = {}
        self.current_music_player = None
        
        self._load_sounds()
        self._subscribe_events()

    def _load_sounds(self):
        sound_dir = GameResources.get("sounds")

        if not sound_dir.exists():
            print(f"Warning: Sound directory not found at {sound_dir}")
            return
            
        for path in sound_dir.iterdir():
            if path.is_file() and path.suffix.lower() in ['.wav', '.mp3', '.ogg']:
                if "music" in path.name.lower() or "soundtrack" in path.name.lower():
                    continue
                    
                key = path.stem 
                self.sounds[key] = arcade.load_sound(str(path))

    def _subscribe_events(self):
        self.event_bus.subscribe(EntityAttackedMeleeEvent, self._on_melee_attack)
        self.event_bus.subscribe(EntityAttackedRangedEvent, self._on_ranged_attack)
        self.event_bus.subscribe(EntityDamagedEvent, self._on_entity_damaged)
        self.event_bus.subscribe(EntityFootstepEvent, self._on_footstep)
        self.event_bus.subscribe(CoinCollectedEvent, self._on_coin_collected)
        
        # New UI and System events
        self.event_bus.subscribe(UIButtonClickEvent, self._on_ui_click)
        self.event_bus.subscribe(PopupOpenedEvent, self._on_popup_opened)
        self.event_bus.subscribe(GameStartedEvent, self._on_game_started)
        self.event_bus.subscribe(ItemBoughtSuccessEvent, self._on_item_bought_success)
        self.event_bus.subscribe(PlayMusicEvent, self._on_play_music)

    def _on_melee_attack(self, event: EntityAttackedMeleeEvent):
        self.play_random_sound("swipe", volume=0.5)

    def _on_ranged_attack(self, event: EntityAttackedRangedEvent):
        self.play_sound("gunshot", volume=0.5)

    def _on_entity_damaged(self, event: EntityDamagedEvent):
        if isinstance(event.entity, Player):
            self.play_random_sound("player_dmg", volume=0.8)
        else:
            self.play_random_sound("enemy_dmg", volume=0.6)

    def _on_footstep(self, event: EntityFootstepEvent):
        if isinstance(event.entity, Player):
            pitch = random.uniform(0.9, 1.1)
            self.play_random_sound("foot_steps", volume=0.3, speed=pitch)

    def _on_coin_collected(self, event: CoinCollectedEvent):
        self.play_sound("coin", volume=0.7)

    def _on_ui_click(self, event: UIButtonClickEvent):
        self.play_sound("ui_button", volume=0.8)
        
    def _on_popup_opened(self, event: PopupOpenedEvent):
        self.play_sound("popup", volume=0.8)
        
    def _on_game_started(self, event: GameStartedEvent):
        self.play_sound("game-start", volume=1.0)
        
    def _on_item_bought_success(self, event: ItemBoughtSuccessEvent):
        self.play_sound("item-bought", volume=0.8)
        
    def _on_play_music(self, event: PlayMusicEvent):
        self.play_music(event.track_name, volume=0.5)

    def play_music(self, name: str, volume: float = 0.5):
        sound_dir = GameResources.get("sounds")
        path = sound_dir / f"{name}.mp3"
        if not path.exists():
            path = sound_dir / f"{name}.wav"
            if not path.exists():
                print(f"Music not found: {name}")
                return
                
        if self.current_music_player:
            self.current_music_player.pause()
            self.current_music_player.delete()
            
        music = arcade.load_sound(str(path), streaming=True)
        self.current_music_player = arcade.play_sound(music, volume=volume, loop=True)

    def play_sound(self, name: str, volume: float = 1.0, speed: float = 1.0):
        sound = self.sounds.get(name)
        if sound:
            arcade.play_sound(sound, volume=volume, speed=speed)
            
    def play_random_sound(self, base_name: str, volume: float = 1.0, speed: float = 1.0):
        matching_keys = [k for k in self.sounds.keys() if k.startswith(base_name)]
        if not matching_keys:
            # Fallback if base_name directly exists
            if base_name in self.sounds:
                self.play_sound(base_name, volume, speed)
            return
            
        chosen_key = random.choice(matching_keys)
        self.play_sound(chosen_key, volume, speed)
