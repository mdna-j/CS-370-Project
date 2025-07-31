
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from login_manager.login_manager import LoginManager
import os
from kivy.lang import Builder


kv_path = os.path.join(os.path.dirname(__file__), "login_screen.kv")
Builder.load_file(kv_path)


class LoginScreen(Screen):
    username_input = ObjectProperty(None)
    password_input = ObjectProperty(None)
    open_popups = []

        ##validate inputs remove invalid char spaces etc

    def login(self):
        if LoginManager.validate(self.username_input,self.password_input) == True:
            if LoginManager.authenticate_user(self.username_input.text, self.password_input.text) is not None:
                self.manager.current = "main"
            else:
                self.show_popup("Login Failed", "Incorrect username or password.")
        else:
            self.manager.current = "login"
            self.show_button_popup()


    def go_to_register(self,instance):
        self.manager.current = "register"

    def show_popup(self, title, message):
        popup=Popup(title=title, content=Label(text=message),auto_dismiss = True, size_hint=(None, None), size=(300, 150))
        popup.open()
        self.open_popups.append(popup)

    def show_button_popup(self):
        butt=Button(text="attempt to register")#made me giggle
        popup=Popup(title = "failed to login",content=butt, auto_dismiss=True, size_hint=(None, None), size=(300, 150))
        butt.bind(on_press=self.go_to_register)
        popup.open()
        self.open_popups.append(popup)

    def dismiss_all_popups(self):
        for popup in self.open_popups:
            popup.dismiss()
        self.open_popups.clear()

    def on_leave(self):
        self.dismiss_all_popups()
