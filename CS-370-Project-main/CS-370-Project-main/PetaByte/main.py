from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from petabyte.login_manager.login_screen import LoginScreen
from petabyte.login_manager.login_manager import LoginManager

class MainScreen(Screen):
    pass

class PetaByteApp(App):
    def build(self):
        LoginManager.initialize()
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))  # Add your real dashboard later
        return sm

if __name__ == "__main__":
    PetaByteApp().run()