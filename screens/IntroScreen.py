from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# Muat file KV untuk IntroScreen
Builder.load_file("kv_files/intro.kv")

class IntroScreen(Screen):
    pass
    def go_to_login(self):
        self.manager.current = 'login'

    
       