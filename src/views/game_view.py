import arcade.color
from arcade import Camera2D

from core.display import BaseView, GameCamera
from services.event_service import EventBus
from services.input.devices.mouse_device import MouseInputDevice

from services.input.input_service import InputService
from services.navigation_service import NavigationService
from services.input.settings.registered_input_contexts import RegisteredInputContexts
from services.input.settings.registered_input_events import TogglePauseInputEvent, ToggleShopInputEvent
from settings.registered_gameplay_events import ToggleShopEvent, RerollShopEvent, PlayMusicEvent, PopupOpenedEvent
from world.level.level_events import LevelChangedEvent
from ui.shop_controller import ShopController
from world.systems.enemy_wave_system import WaveCompleteEvent
from world.systems.shop_system import ShopInstance
from services.input.settings.registered_input_events import ViewportChangedEvent
from world.world_module import World
from ui.hud_controller import HudController
from ui.pause_controller import PauseController


class GameView(BaseView):

    def __init__(self, input_service: InputService, event_bus: EventBus, nav_service: NavigationService):
        super().__init__(input_service)

        self.event_bus = event_bus
        self.nav_service = nav_service

        self.active_keyboard_inputs = set()
        self.world = World(event_bus)
        self.hud = HudController(self.world.player.stats)
        self.pause_menu = PauseController(self, event_bus)
        self.shop_menu = ShopController(event_bus)

        self.world_camera = GameCamera(
            follow_target=self.world.player,
            clamp_rect=self.world.get_level_bounds()
        )
        self.ui_camera = Camera2D()

        self._subscribe_listeners()

    def _subscribe_listeners(self):
        self.event_bus.subscribe(TogglePauseInputEvent, self.on_toggle_pause)
        self.event_bus.subscribe(ToggleShopEvent, self.on_toggle_shop)
        self.event_bus.subscribe(RerollShopEvent, self.on_reroll_shop)
        self.event_bus.subscribe(LevelChangedEvent, self._on_level_changed)
        self.event_bus.subscribe(WaveCompleteEvent, self.hud.update_wave)

    def _unsubscribe_listeners(self):
        self.event_bus.unsubscribe(TogglePauseInputEvent, self.on_toggle_pause)
        self.event_bus.unsubscribe(ToggleShopEvent, self.on_toggle_shop)
        self.event_bus.unsubscribe(RerollShopEvent, self.on_reroll_shop)
        self.event_bus.unsubscribe(LevelChangedEvent, self._on_level_changed)
        self.event_bus.unsubscribe(WaveCompleteEvent, self.hud.update_wave)

    def on_show_view(self):

        self.input_service.enable_context(RegisteredInputContexts.GAMEPLAY)
        self.input_service.enable_context(RegisteredInputContexts.DEBUG)

        self.background_color = arcade.color.BLACK
        self.hud.enable()
        self.event_bus.dispatch(ViewportChangedEvent(self.window.width, self.window.height))
        self.event_bus.dispatch(PlayMusicEvent("soundtrack3-edit"))

    def on_hide_view(self):

        self._unsubscribe_listeners()

        self.input_service.disable_context(RegisteredInputContexts.GAMEPLAY)
        self.input_service.disable_context(RegisteredInputContexts.DEBUG)

        self.hud.disable()
        self.pause_menu.disable()

        self.world.dispose()

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.world_camera.cam.match_window()
        self.ui_camera.match_window()
        # Forzar la actualización de las UIs ocultas
        self.pause_menu.manager.on_resize(width, height)
        self.shop_menu.manager.on_resize(width, height)
        
        # para que los enemigos no spawneen en los bordes de la pantalla antigua
        self.event_bus.dispatch(ViewportChangedEvent(width, height))

    def on_update(self, dt: float):
        super().on_update(dt)

        if not self.pause_menu.is_enabled() and not self.shop_menu.is_enabled():
            self.world.update(dt)
            self.world_camera.update(dt)
            
            # Actualizar HUD -> ahora se actualiza tambien cuando el juego etsa pausado
        if self.world.player:
            from world.systems.combat.entity_stats import StatDefinition
            health = self.world.player.stats.get(StatDefinition.HEALTH)
            max_health = self.world.player.stats.get(StatDefinition.MAX_HEALTH)
            if health is not None and max_health is not None:
                self.hud.set_health(int(health), int(max_health))
            
        self.hud.set_coins(self.world.coins)
        self.hud.update_stats(self.world.player)

    def on_draw(self):
        super().on_draw()

        self.world_camera.use()
        self.world.draw()

        self.ui_camera.use()
        self.hud.draw()

        if self.pause_menu.is_enabled():
            self.pause_menu.draw()

        if self.shop_menu.is_enabled():
            self.shop_menu.draw()

    def on_toggle_pause(self, _: TogglePauseInputEvent):

        if self.pause_menu.is_enabled():
            self.unpause()
        else:
            self.pause()

    def pause(self):

        self.input_service.enable_context(RegisteredInputContexts.PAUSE)

        self.input_service.disable_context(RegisteredInputContexts.GAMEPLAY)
        self.input_service.disable_context(RegisteredInputContexts.DEBUG)

        self.pause_menu.enable()
        self.event_bus.dispatch(PopupOpenedEvent())

    def unpause(self):

        self.input_service.enable_context(RegisteredInputContexts.GAMEPLAY)
        self.input_service.enable_context(RegisteredInputContexts.DEBUG)

        self.input_service.disable_context(RegisteredInputContexts.PAUSE)

        self.pause_menu.disable()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):

        in_world_coords = self.world_camera.cam.unproject((x, y)).xy

        inp = MouseInputDevice.from_button(
            button,
            in_world_coords.x, in_world_coords.y
        )

        self.input_service.register_press(inp)

        # TEMP

    def on_toggle_shop(self, event: ToggleShopEvent):

        if self.shop_menu.is_enabled():
            self.deactivate_shop()
        else:
            self.activate_shop(event.shop)

    def on_reroll_shop(self,event: RerollShopEvent):
        self.shop_menu.reload_items()

    def activate_shop(self, shop: ShopInstance):

        self.input_service.enable_context(RegisteredInputContexts.SHOP)

        self.input_service.disable_context(RegisteredInputContexts.GAMEPLAY)
        self.input_service.disable_context(RegisteredInputContexts.DEBUG)

        self.shop_menu.load_shop(shop)
        self.shop_menu.enable()
        self.event_bus.dispatch(PopupOpenedEvent())

    def deactivate_shop(self):

        self.input_service.enable_context(RegisteredInputContexts.GAMEPLAY)
        self.input_service.enable_context(RegisteredInputContexts.DEBUG)

        self.input_service.disable_context(RegisteredInputContexts.SHOP)

        self.shop_menu.deload_shop()

    def _on_level_changed(self, event: LevelChangedEvent):
        """Actualiza la cámara para ajustarse a los límites del nuevo nivel."""
        self.world_camera = GameCamera(
            follow_target=self.world.player,
            clamp_rect=self.world.get_level_bounds()
        )
        self.world_camera.cam.match_window()