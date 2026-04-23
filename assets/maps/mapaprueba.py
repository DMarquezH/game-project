import arcade
import os
from pathlib import Path


CURRENT_DIR = Path(__file__).parent.resolve()
# Intentamos localizar la carpeta assets subiendo niveles
ASSETS_PATH = CURRENT_DIR.parent 

# --- IMPRESIÓN PARA DEBUG (Esto saldrá en tu terminal) ---
print(f"\n--- DEBUG DE RUTAS ---")
print(f"El script está en: {CURRENT_DIR}")
print(f"Buscando assets en: {ASSETS_PATH}")
print(f"¿Existe la carpeta assets?: {ASSETS_PATH.exists()}")
print(f"----------------------\n")

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Mapa prueba"
TILE_SIZE_FLOOR = 64  
PLAYER_MOVEMENT_SPEED = 5 

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)
        self.scene = None

    def setup(self):
        self.scene = arcade.Scene()

        # Añadido "sprites" a la ruta del jugador y del enemigo
        player_img = (ASSETS_PATH / "sprites" / "entity" / "player_48.png").resolve()
        floor_img = (ASSETS_PATH / "textures" / "map" / "floor_64.png").resolve()
        rock_img = (ASSETS_PATH / "textures" / "map" / "rock_32.png").resolve()
        enemy_img = (ASSETS_PATH / "sprites" / "entity" / "enemy_32.png").resolve()

        # 1. Suelo
        for x in range(0, SCREEN_WIDTH, TILE_SIZE_FLOOR):
            floor = arcade.Sprite(str(floor_img), 1)
            floor.center_x = x + TILE_SIZE_FLOOR / 2
            floor.center_y = TILE_SIZE_FLOOR / 2
            self.scene.add_sprite("Platforms", floor)

        # 2. Rocas
        rock_positions = [[300, 96], [332, 96], [600, 96]] 
        for pos in rock_positions:
            rock = arcade.Sprite(str(rock_img), 1)
            rock.center_x = pos[0]
            rock.center_y = pos[1]
            self.scene.add_sprite("Walls", rock)

        # 3. Jugador
        self.player_sprite = arcade.Sprite(str(player_img), 1)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 150
        self.scene.add_sprite("Player", self.player_sprite)

        # 4. Enemigo
        enemy = arcade.Sprite(str(enemy_img), 1)
        enemy.center_x = 800
        enemy.center_y = 96
        self.scene.add_sprite("Enemies", enemy)

        
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.scene.get_sprite_list("Walls"))

    def on_draw(self):
        self.clear()
        self.scene.draw()

    # --- AÑADE ESTAS TRES FUNCIONES NUEVAS AQUÍ ---

    def on_update(self, delta_time):
        """ Lógica y movimiento. Se ejecuta 60 veces por segundo """
        # Actualiza las físicas, esto mueve al jugador y comprueba las colisiones
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        """ Se llama cuando pulsas una tecla """
        if key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Se llama cuando sueltas una tecla """
        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
