from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App
from auth import AuthService

# Muat file KV untuk RegisterScreen
Builder.load_file("kv_files/register.kv")

# Buat instance AuthService
auth_service = AuthService()

class RegisterScreen(Screen):
    pass
    def register(self, email, password):
        # Daftarkan pengguna dengan role default 'pengguna'
        success, message = auth_service.register(email, password, role='pengguna')
        
        if success:
            print(message)  # Feedback ketika registrasi berhasil
            # Arahkan ke halaman login setelah registrasi berhasil
            App.get_running_app().root.current = 'login'
        else:
            # Menampilkan pesan kesalahan jika registrasi gagal
            print(f"{message}")
            self.show_popup('Pendaftaran Gagal', '')

    def show_popup(self, title, message):
        # Membuat popup untuk menampilkan pesan kesalahan
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def go_back_to_login(self):
        self.manager.current = 'login'