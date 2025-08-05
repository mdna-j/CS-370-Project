import threading
from math import floor
import pixellab
from PIL import Image
from pixellab.animate_with_skeleton import AnimateWithSkeletonResponse
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
import os
from kivy.clock import Clock
from petsystem import pet_screen
from petsystem.pet_screen import PetScreen

kv_path=os.path.join(os.path.dirname(__file__),'pet_generation.kv')
Builder.load_file(kv_path)

class make_pet:

    def __init__(self):
        self.client = pixellab.Client(secret="ce67424e-b79c-4157-93ca-161563c25c67")
        self.petpic = None #must be set by gen_baseImg
        self.animatedpet= None
        self.petidle = None
        self.petanims = []

    def make_pet(self, prompt):

        pet = self.gen_baseimg(prompt)
        print("generating pet image")
        keyposes = self.gen_idle_postions([10, 30, -30])
        print("generating Idle")
        frames = self.Gen_animation(keyposes)
        print("generating animation")
        self.save_as_gif("PetaByte/petsystem/pet.gif")
        print("saved as pet.gif")


    def gen_baseimg(self,prompt: str) -> Image.Image:
        self.petpic = self.client.generate_image_bitforge(
            description=prompt,
            image_size={"width": 128, "height": 128},
            detail="low detail").image.pil_image()
        self.petpic.save("PetaByte/petsystem/pet.png")
        return self.petpic

      # improve return works for now tho just ugly
    def gen_idle_postions(self, pos: list)->list:
        if self.petpic is None:
            raise ValueError("Image not created or initialized run gen_baseimg")
        keypoints = self.client.estimate_skeleton(image=self.petpic).keypoints

        return [
            [
                {
                    "x": kp["x"],
                    "y": kp["y"] + newpose,
                    "label": kp["label"],
                    "z_index": floor(kp["z_index"]),
                }
                for kp in keypoints
            ] for newpose in pos
        ]


    def Gen_animation(self, keyposes: list)->AnimateWithSkeletonResponse:
            self.animatedpet = self.client.animate_with_skeleton(
            image_size={"width": 128, "height": 128},
            skeleton_keypoints=keyposes,
            view="side",
            direction="south",
            reference_image=self.petpic,
            inpainting_images=[None, None, None],
        )
            return self.animatedpet


    def save_as_gif(self,name:str):
        frames = [image.pil_image() for image in self.animatedpet.images]
        self.animatedpet=frames[0].save(name, save_all=True, append_images=frames[1:], duration=250, loop=0,disposal = 2)
        if self.petidle is None:
            self.petidle = self.animatedpet
        self.petanims.append(frames)

class GenScreen(Screen):
    open_popups = []
    def go_to_register(self, *args):
        self.manager.current = "register"

    def go_to_login(self):
        self.manager.current = "login"

    def go_to_pet(self, *args):
            self.manager.current = "petscreen"

    def do_Petgen(self, prompt:str):
        pet=make_pet()
        self.show_button_popup("creating pet a default pet awaits")
        def background_task():
            pet.make_pet(prompt)
            Clock.schedule_once(lambda dt: self.update_pet_image())
        thread1 = threading.Thread(target=background_task)
        thread1.start()

    def update_pet_image(self):
        pet_screen = self.manager.get_screen('petscreen')
        pet_screen.change_pet_image("PetaByte/petsystem/pet.gif")



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

    def show_button_popup(self,msg):
        button = Button(text=msg)
        popup = Popup(
            title="to pet gen",
            content=button,
            auto_dismiss=True,
            size_hint=(None, None),
            size=(300, 150)
        )
        button.bind(on_press=self.go_to_pet)
        popup.open()
        self.open_popups.append(popup)

    def dismiss_all_popups(self):
        for popup in self.open_popups:
            popup.dismiss()
        self.open_popups.clear()

    def on_leave(self):
        self.dismiss_all_popups()
