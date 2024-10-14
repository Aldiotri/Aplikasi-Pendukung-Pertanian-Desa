from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# Muat file KV untuk HomeScreen
Builder.load_file("kv_files/home.kv")

class HomeScreen(Screen):
    pass
    def go_to_search(self):
        self.manager.current = 'search'

    def go_to_cart(self):
        self.manager.current = 'cart'

    def go_to_notification(self):
        self.manager.current = 'notification'

    def go_to_profile(self):
        self.manager.current = 'profile'