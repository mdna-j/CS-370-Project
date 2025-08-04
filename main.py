from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from login_manager.login_screen import LoginScreen
from UI.register_screen import RegisterScreen
from login_manager.login_manager import LoginManager
import sys, os
from petsystem.pet_screen import petscreen
<<<<<<< HEAD

=======
>>>>>>> 3b90b4afa0ca99eaab60b42fb4501e53fa75ff5e

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class MainScreen(Screen):
    pass

class PetaByteApp(App):
    def build(self):
        LoginManager.initialize()
        SM = ScreenManager()
        SM.add_widget(LoginScreen(name='login'))
        SM.add_widget(RegisterScreen(name='register'))
        SM.add_widget(petscreen(name='petscreen'))
        SM.add_widget(MainScreen(name='main'))
        return SM

if __name__ == "__main__":
    PetaByteApp().run()
