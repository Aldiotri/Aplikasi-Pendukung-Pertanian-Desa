from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

class AboutUsScreen(Screen):
    pass
    def go_to_aboutus(self):
        self.manager.current = 'aboutus'
        
    def go_to_profile(self):
        self.manager.current = 'profile'