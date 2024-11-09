from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import firebase_admin
from firebase_admin import credentials, db
from kivy.clock import mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage



# Muat file KV untuk HomeScreen
Builder.load_file("kv_files/home.kv")

class HomeScreen(Screen):
    
    def go_to_search(self):
        self.manager.current = 'search'

    def go_to_cart(self):
        self.manager.current = 'cart'

    def go_to_notification(self):
        self.manager.current = 'notification'

    def go_to_profile(self):
        self.manager.current = 'profile'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fetch_products()
        self.lock_scroll = False  
        

    def fetch_products(self):
        last_scroll_y = self.ids.scrollview.scroll_y
        ref = db.reference('products')  # Menyambung ke node "products" di Firebase
        products = ref.get()  # Mendapatkan data produk

        if products:
            self.display_products(products)
        self.ids.scrollview.scroll_y = last_scroll_y
               
    @mainthread
    def display_products(self, products):
        grid = self.ids.product_grid  # Grid tempat produk ditampilkan
        grid.clear_widgets()

        for key, product in products.items():
            box = BoxLayout(orientation='vertical', size_hint_y=None, height="200dp")
            box.add_widget(AsyncImage(source=product['image_url'], size_hint=(1, 0.8)))
            box.add_widget(Label(text=product['nama'], size_hint=(1, 0.1), color=(1, 1, 1, 1)))
            box.add_widget(Label(text=f"Rp {product['harga']}", size_hint=(1, 0.1), color=(1, 0, 0, 1)))
            grid.add_widget(box)
        