import arcade

class Hurtbox(arcade.SpriteSolidColor):
    def __init__(self, owner, width: int = 32, height: int = 32):
        super().__init__(width=width, height=height, color=(0, 0, 0, 0))
        self.owner = owner

    def sync_position(self):
        if self.owner and getattr(self.owner, "sprite_lists", None):
            self.center_x = self.owner.center_x
            self.center_y = self.owner.center_y
        else:
            self.kill()
