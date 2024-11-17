from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window

# Ukuran perangkat mobile 360x640 (ukuran standar untuk perangkat HD)
Window.size = (360, 640)

# Import screen classes
from screens.LoginScreen import LoginScreen
from screens.RegisterScreen import RegisterScreen
from screens.HomeScreen import HomeScreen
from screens.ProfileScreen import ProfileScreen
from screens.SearchScreen import SearchScreen
from screens.NotificationScreen import NotificationScreen
from screens.CartScreen import CartScreen
from screens.AboutUsScreen import AboutUsScreen
from screens.IntroScreen import IntroScreen
from screens.VerificationScreen import VerificationScreen
from screens.TokosayaScreen import TokosayaScreen
from screens.PesananSayaScreen import PesananSayaScreen
from views import ProductList, AddProduct, EditProduct
from kivy_garden.mapview import MapView
from firebase_admin import credentials, db
import firebase_admin

cred = credentials.Certificate('assets/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://papeda-47fd0-default-rtdb.asia-southeast1.firebasedatabase.app'
})

# Muat kv_files
Builder.load_file("kv_files/intro.kv")
Builder.load_file("kv_files/login.kv")
Builder.load_file("kv_files/register.kv")
Builder.load_file("kv_files/home.kv")
Builder.load_file("kv_files/search.kv")
Builder.load_file("kv_files/cart.kv")
Builder.load_file("kv_files/notification.kv")
Builder.load_file("kv_files/profile.kv")
Builder.load_file("kv_files/aboutus.kv")
Builder.load_file("kv_files/toko.kv")
Builder.load_file("kv_files/verification.kv")
Builder.load_file('kv_files/pesanan_saya.kv')

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        
        # Tambahkan screen ke ScreenManager
        
        sm.add_widget(IntroScreen(name='intro'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(SearchScreen(name='search'))
        sm.add_widget(NotificationScreen(name='notification'))
        sm.add_widget(CartScreen(name='cart'))
        sm.add_widget(AboutUsScreen(name='aboutus'))
        sm.add_widget(VerificationScreen(name='verification'))
        sm.add_widget(TokosayaScreen(name='toko'))
        sm.add_widget(ProductList(name='product_list'))
        sm.add_widget(AddProduct(name='add_product'))
        sm.add_widget(EditProduct(name='edit_product'))
        sm.add_widget(PesananSayaScreen(name='pesanan_saya'))
        
        return sm
    
    
    def update_location(self, map_view):
        current_lat, current_lon = map_view.get_latlon_at(map_view.center_x, map_view.center_y)
        print(f"Current Map Center - Latitude: {current_lat}, Longitude: {current_lon}")

if __name__ == "__main__":
    MainApp().run()
