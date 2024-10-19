from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# Muat file KV untuk CartScreen
Builder.load_file("kv_files/cart.kv")

class CartScreen(Screen):
    pass
    def __init__(self, **kwargs):
        super(CartScreen, self).__init__(**kwargs)
        self.item_count = 1  # Default jumlah item

    def increment_item(self):
        # Tambah jumlah item
        self.item_count += 1
        self.ids.item_count.text = str(self.item_count)

    def decrement_item(self):
        # Kurangi jumlah item, tapi tidak boleh kurang dari 1
        if self.item_count > 1:
            self.item_count -= 1
            self.ids.item_count.text = str(self.item_count)

    def checkout(self):
        # Fungsi ketika tombol checkout ditekan
        print("Checkout dilakukan dengan", self.item_count, "item")
        
    def go_to_search(self):
        self.manager.current = 'search'

    def go_to_home(self):
        self.manager.current = 'home'

    def go_to_notification(self):
        self.manager.current = 'notification'

    def go_to_profile(self):
        self.manager.current = 'profile'