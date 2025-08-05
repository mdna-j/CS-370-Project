from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import NumericProperty
import os

kv_path=os.path.join(os.path.dirname(__file__),'gen_screen.kv')
Builder.load_file(kv_path)

class PetScreen(Screen):
    open_popups = []
    happiness = NumericProperty(50)
    hunger = NumericProperty(50)

    def feed_pet(self):
        print("Feeding pet!")

    def clean_pet(self):
        print("Cleaning pet!")

    def pet_pet(self):
        print("Petting pet!")

    def go_to_register(self, *args):
        self.manager.current = "register"

    def go_to_login(self):
        self.manager.current = "login"

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