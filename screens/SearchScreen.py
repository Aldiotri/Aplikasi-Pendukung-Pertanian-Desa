from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# Muat file KV untuk SearchScreen
Builder.load_file("kv_files/search.kv")

class SearchScreen(Screen):
    pass
    def go_to_home(self):
        self.manager.current = 'home'

    def go_to_cart(self):
        self.manager.current = 'cart'

    def go_to_notification(self):
        self.manager.current = 'notification'

    def go_to_profile(self):
        self.manager.current = 'profile'