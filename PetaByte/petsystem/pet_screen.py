from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, BooleanProperty, StringProperty
from kivy.clock import Clock
import os

from mood_tracker.mood import get_latest_mood  # Make sure this is accessible

kv_path = os.path.join(os.path.dirname(__file__), 'pet_screen.kv')
Builder.load_file(kv_path)

MOOD_EMOJI_MAP = {
    "happy": "😊", "sad": "😢", "neutral": "😐", "productive": "💼",
    "lazy": "😴", "relaxed": "😌", "gaming": "🎮", "social": "💬",
    "creative": "🎨", "browsing": "🌐"
}

class PetScreen(Screen):
    open_popups = []
    happiness = NumericProperty(50)
    hunger = NumericProperty(50)
    current_mood = StringProperty("neutral 😐")

    # Cooldown flags
    feed_cooldown = BooleanProperty(False)
    clean_cooldown = BooleanProperty(False)
    pet_cooldown = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = None

    def set_user_id(self, user_id):
        self.user_id = user_id
        self.update_mood()

    def on_enter(self):
        self.stat_decay_event = Clock.schedule_interval(self.decrease_stats, 10)
        self.mood_refresh_event = Clock.schedule_interval(lambda dt: self.update_mood(), 15)

    def on_leave(self):
        self.dismiss_all_popups()
        if hasattr(self, 'stat_decay_event'):
            self.stat_decay_event.cancel()
        if hasattr(self, 'mood_refresh_event'):
            self.mood_refresh_event.cancel()

    def decrease_stats(self, dt):
        self.hunger = max(0, self.hunger - 5)
        self.happiness = max(0, self.happiness - 3)

    def feed_pet(self):
        if not self.feed_cooldown:
            self.hunger = min(100, self.hunger + 15)
            self.feed_cooldown = True
            self.show_popup("Yum!", "Your pet is full and happy!")
            Clock.schedule_once(self.reset_feed_cooldown, 5)
        else:
            self.show_popup("Too Soon!", "Let your pet digest before feeding again!")

    def clean_pet(self):
        if not self.clean_cooldown:
            self.happiness = min(100, self.happiness + 10)
            self.clean_cooldown = True
            self.show_popup("Clean!", "Your pet feels fresh and happy!")
            Clock.schedule_once(self.reset_clean_cooldown, 5)
        else:
            self.show_popup("Wait!", "You just cleaned your pet!")

    def pet_pet(self):
        if not self.pet_cooldown:
            self.happiness = min(100, self.happiness + 20)
            self.pet_cooldown = True
            self.show_popup("Love!", "Your pet loved the attention!")
            Clock.schedule_once(self.reset_pet_cooldown, 5)
        else:
            self.show_popup("Give it a moment!", "Your pet needs space!")

    def reset_feed_cooldown(self, dt):
        self.feed_cooldown = False

    def reset_clean_cooldown(self, dt):
        self.clean_cooldown = False

    def reset_pet_cooldown(self, dt):
        self.pet_cooldown = False

    def update_mood(self):
        if self.user_id is not None:
            mood = get_latest_mood(self.user_id)
            emoji = MOOD_EMOJI_MAP.get(mood, "😐")
            self.current_mood = f"{mood.capitalize()} {emoji}"

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

    def change_pet_image(self, new_source):
        self.ids.pet.source = new_source
        self.ids.pet.reload()

    def dismiss_all_popups(self):
        for popup in self.open_popups:
            popup.dismiss()
        self.open_popups.clear()
