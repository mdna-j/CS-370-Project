import file
from kivy.app import App
from kivy.lang import Builder
Builder.load_file("gen_screen.kv")
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import NumericProperty
from kivy.lang import Builder
import os

Builder.load_file(os.path.join(os.path.dirname(file), 'path', 'to', 'gen_screen.kv'))

class PetScreen(Screen):
    happiness = NumericProperty(50)
    hunger = NumericProperty(50)

    def feed_pet(self):
       print("Feeding pet!")

    def clean_pet(self):
        print("Cleaning pet!")

    def pet_pet(self):
        print("Petting pet!")