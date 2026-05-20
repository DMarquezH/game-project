import arcade
import arcade.gui

from services.event_service import EventBus, BaseEvent
from services.input.settings.registered_input_events import ToggleShopInputEvent
from settings.game_resources import GameResources
from settings.registered_gameplay_events import RerollShopEvent, BuyItemEvent
from src.ui.base_gui_controller import BaseGuiController
from src.ui.widgets.score_widget import ScoreWidget
from ui.widgets.base_button import BaseButton
from ui.widgets.button_wrapper import ButtonWrapper
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
        btn_nxt = BaseButton(sheet=GameResources.get("textures") / "ui" / "menus" / "button_siguiente_spritesheet.png",sound=GameResources.get("sounds") / "ui" / "button_click.wav",image_width=300,image_height=138,columns=2,count=2,action=lambda:self.event_bus.dispatch(ToggleShopInputEvent()),scale=0.6)
        self.reroll_widget = ScoreWidget(GameResources.get("textures") / "ui" / "hud"/ "coin_highres.png",text=f"{self.shop.current_reroll_cost}Reroll")
        btn_reroll = ButtonWrapper(widget=self.reroll_widget, action=lambda :self.event_bus.dispatch(RerollShopEvent(self.shop)))

        fila_botones.add(btn_nxt)
        fila_botones.add(btn_reroll)

        self.main_layout.add(self.fila_items)
        self.main_layout.add(fila_botones)

        self.reload_items()

        panel_tienda = self.main_layout.with_background(color=arcade.color.DARK_BLUE
        ).with_padding(top=30, left=30, right=30, bottom=30).with_border(width=3, color=arcade.color.GOLD)
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

            text_widget = arcade.gui.UILabel(text=item.name,font_size=18)
            description_widget = arcade.gui.UITextArea(text=item.description,font_size=12,width=150,height=100)
            image_widget = arcade.gui.UIImage(texture=item.texture,width=200,height=200).with_padding(top=10,left=10,right=10,bottom=10).with_border(width=2,color=arcade.color.WHITE)
            price_widget = ScoreWidget(image=GameResources.get("textures") / "ui" / "hud"/ "coin_highres.png",text=str(item.cost))


            box_layout.add(text_widget)
            box_layout.add(description_widget)
            box_layout.add(image_widget)
            # Añadimos un boton en el precio
            buy_button = ButtonWrapper(widget=price_widget,action=lambda: self.event_bus.dispatch(BuyItemEvent(item)))

            box_layout.add(buy_button)

            # Añadimos a la lista activa de items para poder actualizar la tienda luego, aunque no se si es necesario
            self.active_ui.append(box_layout)

        self.reroll_widget.set_text(f"{self.shop.current_reroll_cost}Reroll")
        self.load_items()
    def reroll_shop(self, shop:ShopInstance):
        self.shop = shop
        for i in range(len(shop.active_items)):
            item = shop.active_items[i]
            box_layout = self.used_items[i]
            text_widget = box_layout.children[3] # El orden de los hijos es el mismo que el orden de añadidos, aunque no se si es buena idea fiarse de eso
            description_widget = box_layout.children[2]
            image_widget = box_layout.children[1]
            price_widget = box_layout.children[0].widget # El widget del button wrapper

            text_widget.text = item.name
            description_widget.text = item.description
            image_widget.texture = item.texture
            price_widget.set_text(str(item.cost))

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