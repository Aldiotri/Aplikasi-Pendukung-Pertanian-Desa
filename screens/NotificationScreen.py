from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from firebase_admin import credentials, initialize_app, db
import firebase_admin
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage

class NotificationScreen(Screen):
    def on_enter(self):
        self.load_notifications()

    def load_notifications(self):
        ref = db.reference('/notifications')
        notifications = ref.get()

        self.ids.notification_list.clear_widgets()

        # Menampilkan notifikasi jika ada
        if notifications:
            for key, value in notifications.items():
                notification_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10, size_hint_y=None, height=50)
                notification_layout.add_widget(AsyncImage(source='assets/notification.png', size_hint=(None, None), size=(30, 30)))  # Ukuran ikon lebih kecil

                notification_label = Label(
                    text=value.get('message', 'No Message'),
                    font_size=14,  # Ukuran font lebih kecil agar sesuai dengan layar kecil
                    color=(0, 0, 0, 1),
                    size_hint_y=None,
                    height=40,  # Ukuran label disesuaikan
                    valign='middle',
                    halign='left'
                )
                notification_layout.add_widget(notification_label)
                self.ids.notification_list.add_widget(notification_layout)
        else:
            no_notification_label = Label(
                text="Tidak ada notifikasi",
                font_size=14,
                color=(0.4, 0.4, 0.4, 1),
                size_hint_y=None,
                height=40
            )
            self.ids.notification_list.add_widget(no_notification_label)

        self.load_latest_news()  # Panggil fungsi untuk menampilkan berita terkini

    def load_latest_news(self):
        # Mengambil data berita terkini dari Firebase
        ref = db.reference('/latest_news')
        news_items = ref.get()

        self.ids.latest_news_list.clear_widgets()

        if news_items:
            for key, value in news_items.items():
                news_layout = BoxLayout(orientation='vertical', padding=10, size_hint_y=None, height=90)  # Ukuran BoxLayout lebih kecil
                
                # Judul berita
                title_label = Label(
                    text=value.get('title', 'No Title'),
                    font_size=14,  # Ukuran font judul berita lebih kecil
                    color=(0, 0, 0, 1),
                    size_hint_y=None,
                    height=25,  # Tinggi label lebih kecil
                    bold=True
                )
                news_layout.add_widget(title_label)
                
                # Ringkasan berita
                summary_label = Label(
                    text=value.get('summary', 'No summary available'),
                    font_size=12,  # Ukuran font ringkasan lebih kecil
                    color=(0.5, 0.5, 0.5, 1),
                    size_hint_y=None,
                    height=60  # Tinggi ringkasan disesuaikan
                )
                news_layout.add_widget(summary_label)

                # Tambahkan berita ke dalam daftar berita terkini
                self.ids.latest_news_list.add_widget(news_layout)

        else:
            no_news_label = Label(
                text="Tidak ada berita terkini",
                font_size=14,
                color=(0.4, 0.4, 0.4, 1),
                size_hint_y=None,
                height=40
            )
            self.ids.latest_news_list.add_widget(no_news_label)

    def go_to_search(self):
        self.manager.current = 'search'

    def go_to_cart(self):
        self.manager.current = 'cart'

    def go_to_home(self):
        self.manager.current = 'home'

    def go_to_profile(self):
        self.manager.current = 'profile'