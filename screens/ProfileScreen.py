from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# Muat file KV untuk ProfileScreen
Builder.load_file("kv_files/profile.kv")

class ProfileScreen(Screen):
    pass
    def go_to_search(self):
        self.manager.current = 'search'

    def go_to_cart(self):
        self.manager.current = 'cart'

    def go_to_home(self):
        self.manager.current = 'home'

    def go_to_notification(self):
        self.manager.current = 'notification'