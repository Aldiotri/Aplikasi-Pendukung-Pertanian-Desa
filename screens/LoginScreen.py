from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# Muat file KV untuk LoginScreen
Builder.load_file("kv_files/login.kv")

class LoginScreen(Screen):
    pass
    def login(self):
        self.manager.current = 'home'

    def go_to_register(self):
        self.manager.current = 'register'
       