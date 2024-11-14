from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

class TokosayaScreen(Screen):
    pass
    def go_to_toko(self):
        self.manager.current = 'toko'
        
    def go_to_profile(self):
        self.manager.current = 'profile'
        
    def go_to_product_list(self):
        self.manager.current = 'product_list'