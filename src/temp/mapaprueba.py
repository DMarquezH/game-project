import arcade
from pathlib import Path

# --- CONFIGURACIÓN DE RUTAS (PROYECTO PRINCIPAL) ---
CURRENT_DIR = Path(__file__).parent.resolve()
ASSETS_PATH = CURRENT_DIR.parent 

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "MVP Sandbox - Proyecto Principal"
TILE_SIZE_FLOOR = 64  
PLAYER_MOVEMENT_SPEED = 5  
ESPACIO_EXTRA = 500  

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.scene = None

    def setup(self):
        self.scene = arcade.Scene()

        # Cargamos las imágenes (apuntan correctamente dentro del propio proyecto)
        player_img = (ASSETS_PATH / "sprites" / "entity" / "player_48.png").resolve()
        floor_img = (ASSETS_PATH / "textures" / "level" / "floor_64.png").resolve()
        rock_img = (ASSETS_PATH / "textures" / "level" / "rock_32.png").resolve()
        enemy_img = (ASSETS_PATH / "sprites" / "entity" / "enemy_32.png").resolve()

        # 1. SUELO: Rellenamos la ventana y el espacio extra
        min_x = -ESPACIO_EXTRA
        max_x = SCREEN_WIDTH + ESPACIO_EXTRA
        min_y = -ESPACIO_EXTRA
        max_y = SCREEN_HEIGHT + ESPACIO_EXTRA

        for x in range(min_x, max_x, TILE_SIZE_FLOOR):
            for y in range(min_y, max_y, TILE_SIZE_FLOOR):
                floor = arcade.Sprite(str(floor_img), 1)
                floor.center_x = x + TILE_SIZE_FLOOR / 2
                floor.center_y = y + TILE_SIZE_FLOOR / 2
                self.scene.add_sprite("Background", floor)

        # 2. ROCAS: Bordes INVISIBLES muy alejados de la pantalla
        rock_positions = []
        
        # Muro inferior y superior
        for x in range(min_x, max_x + 32, 32):
            rock_positions.append([x, min_y])  
            rock_positions.append([x, max_y])  
            
        # Muro izquierdo y derecho
        for y in range(min_y, max_y + 32, 32): 
            rock_positions.append([min_x, y])  
            rock_positions.append([max_x, y])  
            
        # Obstáculos centrales (estos SÍ se ven y están dentro de la ventana)
        extra_rocks = [
            [300, 300], [332, 300], [364, 300], [300, 332], [300, 364], 
            [700, 500], [732, 500], [700, 532], [732, 532] 
        ]
        rock_positions.extend(extra_rocks)

        for pos in rock_positions:
            rock = arcade.Sprite(str(rock_img), 1)
            rock.center_x = pos[0]
            rock.center_y = pos[1]
            self.scene.add_sprite("Walls", rock)

        # 3. JUGADOR
        self.player_sprite = arcade.Sprite(str(player_img), 1)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.scene.add_sprite("Player", self.player_sprite)

        # 4. ENEMIGO
        enemy = arcade.Sprite(str(enemy_img), 1)
        enemy.center_x = 800
        enemy.center_y = 150
        self.scene.add_sprite("Enemies", enemy)

        # 5. FÍSICAS
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.scene.get_sprite_list("Walls"))

    def on_draw(self):
        self.clear()
        self.scene.draw()

    def on_update(self, delta_time):
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
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