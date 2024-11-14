from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import firebase_admin
from firebase_admin import credentials, db
from kivy.clock import mainthread
from kivy.uix.image import AsyncImage
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior

class ProductBox(ButtonBehavior, BoxLayout):
    def __init__(self, product, on_click, **kwargs):
        super().__init__(**kwargs)
        self.product = product
        self.on_click = on_click
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = "200dp"

        # Gambar produk
        self.add_widget(AsyncImage(source=product['image_url'], size_hint=(1, 0.8)))

        # Nama dan harga produk
        self.add_widget(Label(text=product['nama'], size_hint=(1, 0.1), color=(1, 1, 1, 1)))
        self.add_widget(Label(text=f"Rp {product['harga']}", size_hint=(1, 0.1), color=(1, 0, 0, 1)))

    def on_release(self):
        self.on_click(self.product)

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
        self.fetch_products()  # Mengambil produk saat HomeScreen dibuat
        self.lock_scroll = False  # Flag untuk scroll

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
            product_box = ProductBox(product, self.show_product_detail)
            grid.add_widget(product_box)

    def show_product_detail(self, product):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Tampilan gambar produk
        layout.add_widget(AsyncImage(source=product['image_url'], size_hint=(1, 0.5)))

        # Detail produk
        layout.add_widget(Label(text=f"Nama: {product['nama']}", font_size="18sp"))
        layout.add_widget(Label(text=f"Harga: Rp {product['harga']}", font_size="18sp"))
        layout.add_widget(Label(text=f"Stok: {product.get('stok', 'Tidak diketahui')}", font_size="18sp"))

        # Tombol untuk checkout dan tambah ke keranjang
        button_layout = BoxLayout(size_hint=(1, 0.2))
        add_to_cart_button = Button(text="Tambah ke Keranjang")
        add_to_cart_button.bind(on_press=lambda x: self.add_to_cart(product))
        button_layout.add_widget(add_to_cart_button)
        button_layout.add_widget(Button(text="Checkout"))
        layout.add_widget(button_layout)

        popup = Popup(title="Detail Produk", content=layout, size_hint=(0.8, 0.8))
        popup.open()

    def add_to_cart(self, product):
        cart_ref = db.reference('cart')  # Akses ke node cart di Firebase
        cart_items = cart_ref.get()  # Ambil data keranjang

        if cart_items:
            # Cek apakah produk sudah ada di keranjang
            for item_id, item_data in cart_items.items():
                if item_data['name'] == product['nama']:
                    # Jika ada, tambahkan quantity
                    new_quantity = item_data['quantity'] + 1
                    item_ref = cart_ref.child(item_id)
                    item_ref.update({'quantity': new_quantity})
                    break
            else:
                # Jika belum ada, tambahkan produk baru
                cart_ref.push({
                    'name': product['nama'],
                    'price': product['harga'],
                    'quantity': 1
                })
        else:
            # Jika keranjang kosong, langsung tambahkan produk
            cart_ref.push({
                'name': product['nama'],
                'price': product['harga'],
                'quantity': 1
            })
