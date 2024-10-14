from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# Muat file KV untuk RegisterScreen
Builder.load_file("kv_files/register.kv")

class RegisterScreen(Screen):
    pass
    def register(self):
        self.manager.current = 'login'

    def go_back_to_login(self):
        self.manager.current = 'login'