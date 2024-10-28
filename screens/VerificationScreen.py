from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# Muat file KV untuk AboutUsScreen
Builder.load_file("kv_files/verification.kv")

class VerificationScreen(Screen):
    pass
    def go_to_verification(self):
        self.manager.current = 'verification'
        
    def go_to_profile(self):
        self.manager.current = 'profile'