from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import os
from login_manager.login_manager import LoginManager


kv_path = os.path.join(os.path.dirname(__file__), "pet_screen.kv")
Builder.load_file(kv_path)

class petscreen(Screen):
    open_popups = []
    def do_register(self, username, password):
        if not username or not password:
            self.show_popup("Error", "Username and password cannot be empty.")
            return
        try:
            LoginManager.register_user(username, password)
            self.show_popup("Success", "User registered successfully!")
            self.manager.current = "login"
        except Exception as e:
            self.show_popup("Registration Error", str(e))

    def go_to_login(self):
        self.manager.current = "login"

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.7, 0.4))
        popup.open()
        self.open_popups.append(popup)

    def dismiss_all_popups(self):
        for popup in self.open_popups:
            popup.dismiss()
        self.open_popups.clear()

    def on_leave(self):
        self.dismiss_all_popups()
