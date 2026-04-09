import arcade

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

WINDOW_TITLE = "survivor-project v0.1"


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

    def on_show_view(self):
        print("GameView")


def main():

    window = arcade.Window()
    view = GameView()

    window.show_view(view)
    arcade.run()


if __name__ == '__main__':
    main()