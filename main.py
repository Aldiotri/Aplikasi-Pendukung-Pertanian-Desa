from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

# Import screen classes
from screens.LoginScreen import LoginScreen
from screens.RegisterScreen import RegisterScreen
from screens.HomeScreen import HomeScreen
from screens.ProfileScreen import ProfileScreen
from screens.SearchScreen import SearchScreen
from screens.NotificationScreen import NotificationScreen
from screens.CartScreen import CartScreen


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        
        # Tambahkan screen ke ScreenManager
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(SearchScreen(name='search'))
        sm.add_widget(NotificationScreen(name='notification'))
        sm.add_widget(CartScreen(name='cart'))
        
        return sm

if __name__ == "__main__":
    MainApp().run()
