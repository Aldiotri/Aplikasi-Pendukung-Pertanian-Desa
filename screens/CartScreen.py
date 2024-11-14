from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.popup import Popup
from firebase_admin import db
from kivy.graphics import Color, RoundedRectangle
import random
from kivy.uix.spinner import Spinner

class CartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_listener()  # Pasang listener untuk pembaruan otomatis

    def setup_listener(self):
        """Pasang listener untuk mendeteksi perubahan pada data keranjang"""
        self.cart_ref = db.reference('cart')
        self.cart_ref.listen(self.on_cart_update)

    def on_cart_update(self, event):
        """Panggil ketika ada pembaruan pada data keranjang"""
        self.load_cart()

    def load_cart(self):
        """Memuat item keranjang dan menampilkan pada UI"""
        self.ids.cart_grid.clear_widgets()  # Menghapus widget yang lama
        cart_items = self.cart_ref.get()  # Mendapatkan data keranjang dari Firebase

        if cart_items:
            for item_id, item_data in cart_items.items():
                item_box = self.create_cart_item(item_data, item_id)
                self.ids.cart_grid.add_widget(item_box)
        else:
            self.ids.cart_grid.add_widget(Label(text="Keranjang Kosong", size_hint_y=None, height=40))

    def create_cart_item(self, item_data, item_id):
        """Membuat BoxLayout untuk setiap item dalam keranjang"""
        item_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=120, padding=10, spacing=10)
        
        with item_box.canvas.before:
            Color(1, 1, 1, 1)  # Warna latar belakang putih
            RoundedRectangle(pos=item_box.pos, size=item_box.size, radius=[10, 10, 10, 10])  # Sudut melengkung
        
        # Gambar produk
        image = AsyncImage(source=item_data.get('image_url', ''), size_hint_x=0.3)
        item_box.add_widget(image)

        # Nama dan jumlah produk
        product_info = BoxLayout(orientation="vertical", size_hint_x=0.4, padding=[5, 0])
        product_info.add_widget(Label(text=f"{item_data['name']}", font_size=18, bold=True, color=(0, 0, 0, 1)))  # Teks hitam
        product_info.add_widget(Label(text=f"Jumlah: {item_data['quantity']}", font_size=14, color=(0.2, 0.2, 0.2, 1)))  # Teks abu-abu
        item_box.add_widget(product_info)

        # Harga produk
        price_label = Label(text=f"Rp {item_data['price']}", size_hint_x=0.2, font_size=16, bold=True, color=(0, 0, 0, 1))  # Teks hitam
        item_box.add_widget(price_label)

        # Tombol kurang dan tambah jumlah
        quantity_layout = BoxLayout(size_hint_x=0.3, spacing=5)
        decrease_button = Button(text="-", on_press=lambda x, item_id=item_id: self.decrease_quantity(item_id), size_hint_y=None, height=40, background_normal='', background_color=(0.8, 0.2, 0.2, 1), color=(1, 1, 1, 1))
        increase_button = Button(text="+", on_press=lambda x, item_id=item_id: self.increase_quantity(item_id), size_hint_y=None, height=40, background_normal='', background_color=(0.2, 0.8, 0.2, 1), color=(1, 1, 1, 1))
        quantity_layout.add_widget(decrease_button)
        quantity_layout.add_widget(Label(text=str(item_data['quantity']), size_hint_x=0.2, font_size=16, color=(0, 0, 0, 1)))  # Teks hitam
        quantity_layout.add_widget(increase_button)
        item_box.add_widget(quantity_layout)

        # Tombol hapus dengan warna merah
        delete_button = Button(text="Hapus", on_press=lambda x, item_id=item_id: self.delete_item(item_id), size_hint_y=None, height=40, background_normal='', background_color=(1, 0.2, 0.2, 1), color=(1, 1, 1, 1))
        item_box.add_widget(delete_button)

        return item_box


    def decrease_quantity(self, item_id):
        """Mengurangi jumlah item dalam keranjang"""
        item_ref = self.cart_ref.child(item_id)
        item_data = item_ref.get()

        if item_data and item_data['quantity'] > 1:
            new_quantity = item_data['quantity'] - 1
            item_ref.update({'quantity': new_quantity})
        else:
            self.delete_item(item_id)

    def increase_quantity(self, item_id):
        """Menambah jumlah item dalam keranjang"""
        item_ref = self.cart_ref.child(item_id)
        item_data = item_ref.get()

        if item_data:
            new_quantity = item_data['quantity'] + 1
            item_ref.update({'quantity': new_quantity})

    def delete_item(self, item_id):
        """Menghapus item dari keranjang"""
        item_ref = self.cart_ref.child(item_id)
        item_ref.delete()

    def format_rupiah(self, angka):
        """Fungsi untuk memformat angka menjadi mata uang Rupiah"""
        return f"Rp {angka:,}".replace(",", ".")
    
    def checkout(self):
        """Menampilkan popup checkout dengan total harga dan informasi tambahan untuk checkout"""
        total_harga = 0
        cart_items = self.cart_ref.get()  # Mengambil data barang dari keranjang

        if cart_items:
            for item_data in cart_items.values():
                total_harga += item_data['price'] * item_data['quantity']

        # Menghasilkan ongkos kirim acak antara Rp.15.000 dan Rp.30.000
        ongkos_kirim = random.randint(15000, 30000)
        total_pembayaran = total_harga + ongkos_kirim

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Menampilkan total harga produk dengan format Rupiah
        layout.add_widget(Label(text=f"Total Harga Produk: {self.format_rupiah(total_harga)}", font_size="18sp"))

        # Menampilkan kolom untuk alamat pengiriman
        layout.add_widget(Label(text="Alamat Pengiriman:", font_size="16sp"))
        alamat_pengiriman = TextInput(hint_text="Masukkan alamat pengiriman", multiline=False, font_size="16sp")
        layout.add_widget(alamat_pengiriman)

        # Menampilkan ongkos kirim dengan format Rupiah
        layout.add_widget(Label(text=f"Ongkos Kirim: {self.format_rupiah(ongkos_kirim)}", font_size="16sp"))

        # Pilihan metode pembayaran
        layout.add_widget(Label(text="Metode Pembayaran:", font_size="16sp"))
        metode_pembayaran = Spinner(
            text="Pilih metode pembayaran",
            values=["COD", "Transfer Bank", "Alfamart/Indomart"],
            size_hint=(1, None),
            height="40dp",
            font_size="16sp",
        )
        layout.add_widget(metode_pembayaran)

        # Menampilkan total pembayaran dengan format Rupiah
        layout.add_widget(Label(text=f"Total Pembayaran: {self.format_rupiah(total_pembayaran)}", font_size="18sp"))

        tombol_checkout = Button(text="Checkout", size_hint=(1, 0.8), font_size="18sp")
        layout.add_widget(tombol_checkout)

        # Menampilkan popup dengan ukuran ramah Android
        popup = Popup(title="Checkout", content=layout, size_hint=(0.9, 0.9), auto_dismiss=True)
        popup.open()

    def refresh_cart(self):
        """Menyegarkan tampilan keranjang"""
        self.load_cart()

    # Navigasi ke layar lain
    def go_to_search(self):
        self.manager.current = 'search'

    def go_to_home(self):
        self.manager.current = 'home'

    def go_to_notification(self):
        self.manager.current = 'notification'

    def go_to_profile(self):
        self.manager.current = 'profile'
