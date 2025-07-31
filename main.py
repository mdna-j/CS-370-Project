from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from login_manager.login_screen import LoginScreen
from UI.register_screen import RegisterScreen
from login_manager.login_manager import LoginManager
import sys, os
import threading
import time
from idle_tracker import track_user_activity, insert_idle_log


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class MainScreen(Screen):
    pass

class PetaByteApp(App):
    def build(self):
        LoginManager.initialize()
        SM = ScreenManager()
        SM.add_widget(LoginScreen(name='login'))
        SM.add_widget(RegisterScreen(name='register'))
        SM.add_widget(MainScreen(name='main'))
        return SM

def background_idle_monitor(user_id):
    last_app = None
    while True:
        mood_log = track_user_activity(duration_sec=60, interval_sec=5)
        for timestamp, app_name, mood in mood_log:
            if app_name != last_app:  # only log if app changed
                insert_idle_log(user_id, timestamp, app_name, mood)
                last_app = app_name
        time.sleep(600)  # Wait 10 minutes before the next scan

if __name__ == "__main__":
    PetaByteApp().run()
