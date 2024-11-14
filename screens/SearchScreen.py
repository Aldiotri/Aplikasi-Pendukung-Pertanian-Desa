from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import firebase_admin
from firebase_admin import credentials, db
from kivy.clock import mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage


class SearchScreen(Screen):
    pass
    def go_to_home(self):
        self.manager.current = 'home'

    def go_to_cart(self):
        self.manager.current = 'cart'

    def go_to_notification(self):
        self.manager.current = 'notification'

    def go_to_profile(self):
        self.manager.current = 'profile'
        
    # Di dalam SearchScreen.py
    def search_products(self, search_query):
        # Mendapatkan referensi ke database (Realtimedatabase atau Firestore)
        products_ref = db.reference('products')  # Ganti dengan referensi yang sesuai untuk Realtime Database atau Firestore
        
        # Menampilkan produk yang cocok dengan pencarian
        products = products_ref.order_by_child('nama').start_at(search_query).end_at(search_query + '\uf8ff').get()
        
        # Menampilkan hasil pencarian
        for product in products.values():
            print(product['nama'], product['harga'])


        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fetch_products()

    def fetch_products(self):
        ref = db.reference('products')  # Menyambung ke node "products" di Firebase
        products = ref.get()  # Mendapatkan data produk

        if products:
            self.display_products(products)

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
        
    