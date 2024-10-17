from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
# Muat file KV untuk ProfileScreen
Builder.load_file("kv_files/profile.kv")

class ProfileScreen(Screen):
    pass
    def open_logout_popup(self):
        # Membuat konten popup
        popup_content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Tambahkan Label
        popup_content.add_widget(Label(text="Apakah Anda yakin ingin logout?", font_size='18sp'))

        # Tombol untuk mengonfirmasi atau membatalkan logout
        button_layout = BoxLayout(spacing=10, size_hint_y=None, height='50dp')

        # Tombol konfirmasi logout
        confirm_btn = Button(text="Logout", size_hint=(0.5, 1), background_color=(1, 0.3, 0.3, 1))
        confirm_btn.bind(on_press=self.logout)  # 'self.logout' untuk memanggil metode
        button_layout.add_widget(confirm_btn)

        # Tombol untuk membatalkan
        cancel_btn = Button(text="Batal", size_hint=(0.5, 1))
        cancel_btn.bind(on_press=self.dismiss_popup)  # 'self.dismiss_popup' untuk memanggil metode
        button_layout.add_widget(cancel_btn)

        # Tambahkan tombol ke layout popup
        popup_content.add_widget(button_layout)

        # Membuat dan menampilkan popup
        self.popup = Popup(title="Konfirmasi Logout", content=popup_content, size_hint=(0.8, 0.4), auto_dismiss=False)
        self.popup.open()

    def dismiss_popup(self, *args):
        # Menutup popup
        self.popup.dismiss()

    def logout(self, *args):
        # Proses logout
        print("Logout berhasil.")
        self.dismiss_popup()  # Menutup popup setelah logout
        self.manager.current = 'login'
    
    
    def go_to_search(self):
        self.manager.current = 'search'

    def go_to_cart(self):
        self.manager.current = 'cart'

    def go_to_home(self):
        self.manager.current = 'home'

    def go_to_notification(self):
        self.manager.current = 'notification'
        
    def go_to_aboutus(self):
        self.manager.current = 'aboutus'