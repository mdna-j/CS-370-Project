from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import os

# Loads the corresponding KV file
kv_path = os.path.join(os.path.dirname(__file__), "main_screen.kv")
Builder.load_file(kv_path)

class MainScreen(Screen):

    def on_enter(self):
        # You can initialize any screen data here
        print("Main screen loaded")
