from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from login_manager.login_manager import LoginManager
import os
from kivy.lang import Builder
import threading
from idle_tracker import track_user_activity  # Import your background function


kv_path = os.path.join(os.path.dirname(__file__), "login_screen.kv")
Builder.load_file(kv_path)

class LoginScreen(Screen):
    username_input = ObjectProperty(None)
    password_input = ObjectProperty(None)

    def login(self):
        if LoginManager.authenticate_user(self.username_input.text, self.password_input.text):
            self.manager.current = "main"
            # ✅ Start background thread after login
            idle_thread = threading.Thread(target=track_user_activity, args=(id,))
            idle_thread.daemon = True
            idle_thread.start()
        else:
            self.show_popup("Login Failed", "Incorrect username or password.")

    def go_to_register(self):
        self.manager.current = "register"

    def show_popup(self, title, message):
        Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(300, 150)).open()
