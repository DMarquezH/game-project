import arcade
import arcade.gui

from services.event_service import EventBus, BaseEvent

from settings.game_resources import GameResources
from settings.registered_gameplay_events import RerollShopEvent, BuyItemEvent, ToggleShopEvent
from ui.base_gui_controller import BaseGuiController
from ui.widgets.score_widget import ScoreWidget
from ui.widgets.base_button import BaseButton
from world.systems.shop_system import ShopInstance


class ShopController(BaseGuiController):

    def __init__(self,event_bus: EventBus):
        super().__init__()
        self.main_layout = None
        self.event_bus = event_bus
        self.enabled = False
        self.shop: ShopInstance | None = None
        self.active_ui: list[arcade.gui.UIBoxLayout]= [] # Lista de box_layout activos para actualizar la tienda
        self.fila_items: arcade.gui.UIBoxLayout | None = None
        self.reroll_widget: ScoreWidget | None = None

    def load_shop(self, shop: ShopInstance):
        self.manager.clear()
        self.shop = shop
        self.main_layout = arcade.gui.UIBoxLayout(vertical=True, space_between=40) # .withBackground

        self.fila_items = arcade.gui.UIBoxLayout(vertical=False,space_between=30)

        fila_botones = arcade.gui.UIBoxLayout(vertical=False, space_between=20)
        btn_nxt = BaseButton(
            sheet=GameResources.get("textures") / "ui" / "menus" / "button_siguiente_spritesheet.png",
            event_bus=self.event_bus,
            image_width=300,
            image_height=138,
            columns=2,
            count=2,
            action=lambda:self.event_bus.dispatch(ToggleShopEvent(self.shop)),
            scale=0.8
        )
        self.reroll_widget = ScoreWidget(GameResources.get("textures") / "ui" / "hud"/ "coin_highres.png",text=f"{self.shop.current_reroll_cost} Reroll")

        btn_reroll = BaseButton(
            widget=self.reroll_widget,
            action= lambda: self.event_bus.dispatch(RerollShopEvent(self.shop)),
            sheet= GameResources.get("textures") /"ui" / "menus" / "base_button.png",
            image_width= 300,
            image_height= 138,
            columns=2,
            count=2,
            event_bus=self.event_bus,
            scale = 0.8
        )

        fila_botones.add(btn_nxt)
        fila_botones.add(btn_reroll)

        self.main_layout.add(self.fila_items)
        self.main_layout.add(fila_botones)

        self.reload_items()

        panel_tienda = (self.main_layout.with_background(texture=arcade.load_texture(GameResources.get("textures") / "ui" /"menus"/"shop_background.png"))
                        .with_padding(top=80, left=80, right=80, bottom=80))
        ancla = arcade.gui.UIAnchorLayout()
        ancla.add(child= panel_tienda,anchor_x="center",anchor_y="center")
        self.manager.add(ancla)
        self.enable()
        self.enabled = True

    def load_items(self):
        self.fila_items.clear()
        for item in self.active_ui:
            self.fila_items.add(item)

    def reload_items(self):

        self.active_ui.clear()
        for item in self.shop.active_items:
            box_layout = arcade.gui.UIBoxLayout(vertical=True,space_between= 10,width=100,height=300)

            text_widget = arcade.gui.UILabel(text=item.name,font_size=16,align="center",font_name="Black Ops One")
            description_widget = arcade.gui.UITextArea(text=item.description,font_size=12,width=150,height=50)
            image_widget = arcade.gui.UIImage(texture=item.texture,width=200,height=200).with_padding(top=10,left=10,right=10,bottom=10)
            price_widget = ScoreWidget(image=GameResources.get("textures") / "ui" / "hud"/ "coin_highres.png",text=str(item.cost))


            box_layout.add(text_widget)
            box_layout.add(description_widget)
            box_layout.add(image_widget)
            # Añadimos un boton en el precio

            buy_button = BaseButton(
                widget=price_widget,
                action=lambda it=item: self.event_bus.dispatch(BuyItemEvent(item=it,shop=self.shop)),
                sheet=GameResources.get("textures") / "ui" / "menus" / "base_button.png",
                image_width=300,
                image_height=138,
                columns=2,
                count=2,
                scale= 0.8
            )
            box_layout.add(buy_button)

            # Añadimos a la lista activa de items para poder actualizar la tienda luego
            self.active_ui.append(box_layout)

        self.reroll_widget.set_text(f"{self.shop.current_reroll_cost} Reroll")
        self.load_items()

    def deload_shop(self):
        self.shop = None
        self.manager.clear()
        self.main_layout = None
        self.disable()
        self.enabled = False

    def is_enabled(self) -> bool:
        return self.enabled

    def enable(self):
        super().enable()