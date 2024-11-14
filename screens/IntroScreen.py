from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

class IntroScreen(Screen):
    pass
    def go_to_login(self):
        self.manager.current = 'login'

    
       