import arcade

def main():
    print("Testing SpriteSolidColor kwargs...")
    try:
        s = arcade.SpriteSolidColor(width=32, height=32, color=(0, 0, 0, 0))
        print("Position kwargs:", s.position)
    except Exception as e:
        print("Error with SpriteSolidColor kwargs:", e)

    print("Testing Sprite with explicit texture...")
    try:
        tex = arcade.Texture.create_empty("dummy", (32, 32))
        s2 = arcade.Sprite()
        s2.texture = tex
        print("Position 2:", s2.position)
    except Exception as e:
        print("Error with explicit texture:", e)

main()
