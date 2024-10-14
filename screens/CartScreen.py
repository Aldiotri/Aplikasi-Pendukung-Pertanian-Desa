from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# Muat file KV untuk CartScreen
Builder.load_file("kv_files/cart.kv")

class CartScreen(Screen):
    pass
    def go_to_search(self):
        self.manager.current = 'search'

    def go_to_home(self):
        self.manager.current = 'home'

    def go_to_notification(self):
        self.manager.current = 'notification'

    def go_to_profile(self):
        self.manager.current = 'profile'