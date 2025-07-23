from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from login_manager.login_screen import LoginScreen
from UI.register_screen import RegisterScreen
from login_manager.login_manager import LoginManager
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class MainScreen(Screen):
    pass

class PetaByteApp(App):
    def build(self):
        LoginManager.initialize()
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == "__main__":
    PetaByteApp().run()
