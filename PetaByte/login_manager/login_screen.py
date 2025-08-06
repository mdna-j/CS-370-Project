from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from login_manager.login_manager import LoginManager
import os
from kivy.lang import Builder
import threading
from idle_tracker.idle import track_user_activity

kv_path = os.path.join(os.path.dirname(__file__), "login_screen.kv")
Builder.load_file(kv_path)

class LoginScreen(Screen):
    username_input = ObjectProperty(None)
    password_input = ObjectProperty(None)
    open_popups = []

    def login(self):
        username = self.username_input.text
        password = self.password_input.text

        # Input validation
        if hasattr(LoginManager, 'validate') and not LoginManager.validate(self.username_input, self.password_input):
            self.show_button_popup()
            return

        # Authenticate user
        if LoginManager.authenticate_user(username, password):
            user_id = LoginManager.get_user_id(username)

            # Pass user_id to PetScreen and switch screens
            pet_screen = self.manager.get_screen("petscreen")
            if user_id is not None:
                pet_screen.set_user_id(user_id)

                # Start idle tracking in background
                idle_thread = threading.Thread(target=track_user_activity, args=(user_id,))
                idle_thread.daemon = True
                idle_thread.start()

            self.go_to_generate()
        else:
            self.show_popup("Login Failed", "Incorrect username or password.")

    def go_to_register(self, *args):
        self.manager.current = "register"

    def go_to_generate(self, *args):
        self.manager.current = "petscreen"

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            auto_dismiss=True,
            size_hint=(None, None),
            size=(300, 150)
        )
        popup.open()
        self.open_popups.append(popup)

    def show_button_popup(self):
        button = Button(text="Attempt to Register")
        popup = Popup(
            title="Failed to Login",
            content=button,
            auto_dismiss=True,
            size_hint=(None, None),
            size=(300, 150)
        )
        button.bind(on_press=self.go_to_register)
        popup.open()
        self.open_popups.append(popup)

    def dismiss_all_popups(self):
        for popup in self.open_popups:
            popup.dismiss()
        self.open_popups.clear()

    def on_leave(self):
        self.dismiss_all_popups()

    def forgot_password(self):
        from kivy.uix.textinput import TextInput
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)

        username_input = TextInput(hint_text="Enter username", multiline=False)
        new_password_input = TextInput(hint_text="Enter new password", multiline=False, password=True)

        box.add_widget(username_input)
        box.add_widget(new_password_input)

        def reset(_):
            username = username_input.text.strip()
            new_password = new_password_input.text.strip()
            if username and new_password:
                success = LoginManager.reset_password(username, new_password)
                message = "Password reset successful!" if success else "Username not found!"
                self.show_popup("Reset Status", message)
                popup.dismiss()

        confirm_btn = Button(text="Reset Password", on_press=reset)
        box.add_widget(confirm_btn)

        popup = Popup(title="Forgot Password?", content=box, size_hint=(None, None), size=(400, 250))
        popup.open()
