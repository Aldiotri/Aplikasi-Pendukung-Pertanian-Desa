from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from firebase_admin import credentials, initialize_app, db
import firebase_admin
from kivy.uix.label import Label

class NotificationScreen(Screen):
    def on_enter(self):
        # Memuat notifikasi dari Firebase ketika layar dibuka
        self.load_notifications()

    def load_notifications(self):
        ref = db.reference('/notifications')
        notifications = ref.get()

        # Menghapus notifikasi lama dari tampilan
        self.ids.notification_list.clear_widgets()

        # Cek jika notifications tidak kosong atau None
        if notifications:
            for key, value in notifications.items():
                notifikasi = Label(
                    text=value.get('message', 'No Message'),
                    font_size=16,
                    color=(0, 0, 0, 1),
                    size_hint_y=None,
                    height=40
                )
                self.ids.notification_list.add_widget(notifikasi)
        else:
            # Jika tidak ada notifikasi, tambahkan teks "Tidak ada notifikasi"
            no_notification_label = Label(
                text="Tidak ada notifikasi",
                font_size=16,
                color=(0.4, 0.4, 0.4, 1),
                size_hint_y=None,
                height=40
            )
            self.ids.notification_list.add_widget(no_notification_label)


    def go_to_search(self):
        self.manager.current = 'search'

    def go_to_cart(self):
        self.manager.current = 'cart'

    def go_to_home(self):
        self.manager.current = 'home'

    def go_to_profile(self):
        self.manager.current = 'profile'