from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

class NotificationScreen(Screen):
    pass
    def go_to_search(self):
        self.manager.current = 'search'

    def go_to_cart(self):
        self.manager.current = 'cart'

    def go_to_home(self):
        self.manager.current = 'home'

    def go_to_profile(self):
        self.manager.current = 'profile'