from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from auth import AuthService
from kivy.uix.popup import Popup
from kivy.uix.label import Label

# Muat file KV untuk LoginScreen
Builder.load_file("kv_files/login.kv")
# Builder.load_file("kv_files/home.kv")

# Buat instance AuthService
auth_service = AuthService()

class LoginScreen(Screen):
    pass
    def login(self, email, password):
        # Panggil metode login dari auth_service
        success, message = auth_service.login(email, password)
        
        if success:
            # Semua pengguna diarahkan ke satu layar, misalnya `home_screen`
            App.get_running_app().root.current = 'home'
        else:
            # Menampilkan pesan kesalahan login
            print(f"{message}")
            self.show_popup('Login Gagal', '')

    def show_popup(self, title, message):
        # Membuat popup untuk menampilkan pesan
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()
            
    def go_to_register(self):
        self.manager.current = 'register'
        
    def go_to_intro(self):
        self.manager.current = 'intro'
       