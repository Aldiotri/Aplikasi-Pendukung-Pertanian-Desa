from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from firebase_admin import db
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.clock import mainthread
from kivy.uix.popup import Popup
from kivy.uix.button import Button
import random
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from datetime import datetime
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
        self.add_widget(Label(text=product['nama'], size_hint=(1, 0.1), color=(0, 0, 0, 1)))
        self.add_widget(Label(text=f"Rp {product['harga']}", size_hint=(1, 0.1), color=(1, 0, 0, 1)))

    def on_release(self):
        self.on_click(self.product)
        
class SearchScreen(Screen):
    def go_to_home(self):
        self.manager.current = 'home'

    def go_to_cart(self):
        self.manager.current = 'cart'

    def go_to_notification(self):
        self.manager.current = 'notification'

    def go_to_profile(self):
        self.manager.current = 'profile'
        
    # Fungsi untuk mencari produk berdasarkan query
    def search_products(self, search_query):
        products_ref = db.reference('products')
        products = products_ref.order_by_child('nama').start_at(search_query).end_at(search_query + '\uf8ff').get()

        if products:
            self.display_products(products)
        else:
            print("Tidak ada produk yang ditemukan.")

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
        layout.add_widget(Label(text=f"Harga: Rp {product['harga']:,}".replace(",", "."), font_size="18sp"))
        layout.add_widget(Label(text=f"Stok: {product.get('stok', 'Tidak diketahui')}", font_size="18sp"))

        # Tombol untuk checkout dan tambah ke keranjang
        button_layout = BoxLayout(size_hint=(1, 0.5))
        add_to_cart_button = Button(text="Masukkan Keranjang")
        add_to_cart_button.bind(on_press=lambda x: self.add_to_cart(product))
        button_layout.add_widget(add_to_cart_button)

        checkout_button = Button(text="Checkout")
        checkout_button.bind(on_press=lambda x: self.checkout_popup(product))
        button_layout.add_widget(checkout_button)

        layout.add_widget(button_layout)
        popup = Popup(title="Detail Produk", content=layout, size_hint=(0.8, 0.8))
        popup.open()

    def checkout_popup(self, product):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        ongkos_kirim = random.randint(15000, 30000)
        total_harga = product['harga']
        total_pembayaran = total_harga + ongkos_kirim

        layout.add_widget(Label(text=f"Total Harga Produk: Rp {total_harga:,}".replace(",", "."), font_size="18sp"))

        alamat_pengiriman = TextInput(hint_text="Masukkan alamat pengiriman", multiline=False, font_size="16sp")
        layout.add_widget(Label(text="Alamat Pengiriman:", font_size="16sp"))
        layout.add_widget(alamat_pengiriman)

        layout.add_widget(Label(text=f"Ongkos Kirim: Rp {ongkos_kirim:,}".replace(",", "."), font_size="16sp"))

        metode_pembayaran = Spinner(
            text="Pilih metode pembayaran",
            values=["COD", "Transfer Bank", "Alfamart/Indomart"],
            size_hint=(1, None),
            height="40dp",
            font_size="16sp",
        )
        layout.add_widget(Label(text="Metode Pembayaran:", font_size="16sp"))
        layout.add_widget(metode_pembayaran)

        layout.add_widget(Label(text=f"Total Pembayaran: Rp {total_pembayaran:,}".replace(",", "."), font_size="18sp"))

        tombol_checkout = Button(text="Buat Pesanan", size_hint=(1, 0.8), font_size="18sp")
        tombol_checkout.bind(on_press=lambda x: self.create_order(product, alamat_pengiriman.text, ongkos_kirim, total_pembayaran, metode_pembayaran.text))
        layout.add_widget(tombol_checkout)

        popup = Popup(title="Checkout", content=layout, size_hint=(0.9, 0.9))
        popup.open()

    def create_order(self, product, alamat_pengiriman, ongkos_kirim, total_pembayaran, metode_pembayaran):
        order_ref = db.reference('orders')
        order_data = {
            'product_name': product['nama'],
            'price': product['harga'],
            'shipping_cost': ongkos_kirim,
            'total_payment': total_pembayaran,
            'shipping_address': alamat_pengiriman,
            'payment_method': metode_pembayaran,
            'timestamp': datetime.now().isoformat()
        }
        order_ref.push(order_data)

        # Tambahkan data checkout ke notifikasi di Firebase
        notification_ref = db.reference('/notifications')
        notification_data = {
            'message': f"Pesanan untuk {product['nama']} berhasil dibuat dengan total pembayaran Rp {total_pembayaran:,}".replace(",", "."),
            'timestamp': datetime.now().isoformat()
        }
        notification_ref.push(notification_data)
        
        # Tampilkan popup atau dialog sukses
        success_popup = Popup(title="Pesanan Berhasil", content=Label(text="Pesanan Anda berhasil dibuat!"), size_hint=(0.7, 0.4))
        success_popup.open()

    def add_to_cart(self, product):
        """Menambahkan produk ke keranjang di Firebase, termasuk foto produk"""
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
                    'quantity': 1,
                    'image_url': product['image_url']  # Menyimpan URL gambar produk
                })
        else:
            # Jika keranjang kosong, langsung tambahkan produk
            cart_ref.push({
                'name': product['nama'],
                'price': product['harga'],
                'quantity': 1,
                'image_url': product['image_url']  # Menyimpan URL gambar produk
            })