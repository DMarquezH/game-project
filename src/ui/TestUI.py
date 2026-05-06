from src.services.navigation import NavigationService


class TestUI:

    def __init__(self, nav_service: NavigationService):
        self.nav_service = nav_service

    def nav_to_main_menu(self):
        self.nav_service.navigate("main_menu")