from kivy.uix.screenmanager import Screen
from kivy.clock import mainthread
from kivy.uix.boxlayout import BoxLayout
from firebase_admin import db
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.label import Label

class CustomOrderBox(BoxLayout):
    product_name = StringProperty("")
    price = NumericProperty(0)
    quantity = NumericProperty(1)
    status = StringProperty("")

    def confirm_receipt(self):
        order_ref = db.reference(f"orders/{self.order_id}")
        order_ref.update({"status": "Beri Penilaian"})

    def make_payment(self):
        order_ref = db.reference(f"orders/{self.order_id}")
        order_ref.update({"status": "Dikemas"})

class PesananSayaScreen(Screen):
    def go_to_pesanan_saya(self):
        self.manager.current = 'pesanan_saya'

    def go_to_profile(self):
        self.manager.current = 'profile'

    def fetch_orders(self):
        ref = db.reference('orders')
        orders = ref.get()  # Mengambil data pesanan dari Firebase

        if orders:
            self.display_orders(orders)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fetch_orders()

    @mainthread
    def display_orders(self, orders):
        unpaid_box = self.ids.unpaid_box
        packed_box = self.ids.packed_box
        shipped_box = self.ids.shipped_box
        review_box = self.ids.review_box

        # Bersihkan tampilan di setiap tab status
        unpaid_box.clear_widgets()
        packed_box.clear_widgets()
        shipped_box.clear_widgets()
        review_box.clear_widgets()

        for order_id, order_data in orders.items():
            # Tentukan status dengan default jika kunci 'status' tidak ada
            status = order_data.get('status', 'Belum Dibayar')

            order_box = CustomOrderBox(
                product_name=order_data.get("nama", "Produk"),
                price=order_data.get("harga", 0),
                quantity=order_data.get("quantity", 1),
                status=status,
            )
            order_box.order_id = order_id  # Menyimpan ID pesanan

            # Menambahkan item ke tab sesuai status
            if status == 'Belum Dibayar':
                unpaid_box.add_widget(order_box)
            elif status == 'Dikemas':
                packed_box.add_widget(order_box)
            elif status == 'Dikirim':
                shipped_box.add_widget(order_box)
            elif status == 'Beri Penilaian':
                review_box.add_widget(order_box)

        # Menampilkan pesan kosong jika tidak ada pesanan
        if not unpaid_box.children:
            unpaid_box.add_widget(self.create_empty_label("Tidak ada pesanan yang belum dibayar"))
        if not packed_box.children:
            packed_box.add_widget(self.create_empty_label("Tidak ada pesanan dikemas"))
        if not shipped_box.children:
            shipped_box.add_widget(self.create_empty_label("Tidak ada pesanan dikirim"))
        if not review_box.children:
            review_box.add_widget(self.create_empty_label("Tidak ada pesanan yang perlu diberi penilaian"))

    def create_empty_label(self, text):
        """Membuat Label untuk ditampilkan saat tidak ada pesanan."""
        return Label(text=text, color=(0.5, 0.5, 0.5, 1), font_size="16sp")
