

import random
import arcade


class DamageNumber:
    def __init__(self, text: str, x: float, y: float, color, is_critical: bool):
        font_size = 18 if is_critical else 14
        x += random.uniform(-15, 15)
        y += random.uniform(-10, 10)
        self.text = arcade.Text(text, x, y, color, font_size=font_size, bold=is_critical, anchor_x="center", anchor_y="center")
        self.timer = 0.0
        self.lifetime = 0.8
        self.velocity_y = 60.0
        self.velocity_x = random.uniform(-20, 20)
        self.alpha = 255

    def update(self, delta_time: float):
        self.timer += delta_time
        self.text.x += self.velocity_x * delta_time
        self.text.y += self.velocity_y * delta_time
        
        ratio = max(0.0, 1.0 - (self.timer / self.lifetime))
        self.alpha = int(255 * ratio)
        self.text.color = (self.text.color[0], self.text.color[1], self.text.color[2], self.alpha)

    def draw(self):
        self.text.draw()