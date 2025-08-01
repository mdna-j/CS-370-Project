from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from login_manager.login_screen import LoginScreen
from UI.register_screen import RegisterScreen
from login_manager.login_manager import LoginManager
import sys, os
from petsystem.pet_screen import petscreen

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class MainScreen(Screen):
    pass

class PetaByteApp(App):
    def build(self):
        LoginManager.initialize()
        SM = ScreenManager()
        SM.add_widget(LoginScreen(name='login'))
        SM.add_widget(RegisterScreen(name='register'))
        SM.add_widget(petscreen(name='pet screen'))
        SM.add_widget(MainScreen(name='main'))
        return SM

if __name__ == "__main__":
    PetaByteApp().run()
