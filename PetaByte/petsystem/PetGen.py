from math import floor

import pixellab
from PIL import Image
from pixellab.animate_with_skeleton import AnimateWithSkeletonResponse


class make_pet:

    def __init__(self):
        self.client = pixellab.Client(secret="ce67424e-b79c-4157-93ca-161563c25c67")
        self.petpic = None #must be set by gen_baseImg
        self.animatedpet= None
        self.petidle = None
        self.petanims = []


    def gen_baseimg(self,prompt: str) -> Image.Image:
        self.petpic = self.client.generate_image_bitforge(
            description=prompt,
            image_size={"width": 128, "height": 128},
            detail="low detail").image.pil_image()
        self.petpic.save("pet.png")
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


"""
pil_image = make_pet.gen_img("cute red dragon ")
pil_image.save("default_pet.png")

skeleton_response = client.estimate_skeleton(make_pet.gen_baseimg("cute red dragon "))
raw_keypoints = skeleton_response.keypoints


def get_scaled_keypoints(offset_y=0):
    return [
        {
            "x": kp["x"],
            "y": kp["y"] + offset_y,
            "label": kp["label"],
            "z_index": floor(kp["z_index"]),
        }
        for kp in raw_keypoints
    ]


# Step 4: Create breathing/idle animation keyframes
skeleton_keypoints = [
    get_scaled_keypoints(0),
    get_scaled_keypoints(20),
    get_scaled_keypoints(-20),
    # get_scaled_keypoints(-2),
]
"""
#run
newpet = make_pet()
pet = newpet.gen_baseimg("red dragon with wings")
print("generating pet image")
keyposes = newpet.gen_idle_postions([10,30,-30])
print("generating Idle")
frames = newpet.Gen_animation(keyposes)
print("generating animation")
newpet.save_as_gif("pet.gif")
print("saved as pet.gif")
