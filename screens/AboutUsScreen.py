from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# Muat file KV untuk HomeScreen
Builder.load_file("kv_files/home.kv")

class AboutUsScreen(Screen):
    pass
    def go_to_aboutus(self):
        self.manager.current = 'aboutus'
        
    def go_to_profile(self):
        self.manager.current = 'profile'