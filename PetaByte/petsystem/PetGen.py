from math import floor

import pixellab
from PIL import Image
import json
import math

client = pixellab.Client(secret="ce67424e-b79c-4157-93ca-161563c25c67")


reference_response= client.generate_image_bitforge(
    description="cute 8-bit pixel art dragon",
    image_size={"width": 128, "height": 128},
)

pil_image= reference_response.image.pil_image()
pil_image.save("cute_dragon_transparent.png")
pil_image.show()


skeleton_response = client.estimate_skeleton(image=pil_image)
raw_keypoints = skeleton_response.keypoints
print(json.dumps(raw_keypoints, indent=2))

def get_scaled_keypoints(offset_y=0.0):
    return [
        {
            "x": kp["x"] ,
            "y": kp["y"] + offset_y,
            "label": kp["label"],
            "z_index": floor(kp["z_index"]),
        }
        for kp in raw_keypoints
    ]

# Step 4: Create breathing/idle animation keyframes
skeleton_keypoints = [
    #get_scaled_keypoints(0),
    get_scaled_keypoints(2),
    #get_scaled_keypoints(0),
    #get_scaled_keypoints(-2),
]
#inpainting_images = [pil_image.copy() for _ in skeleton_keypoints]
print(json.dumps(skeleton_keypoints[0], indent=2))

animation_response = client.animate_with_skeleton(

    image_size={"width": 128, "height": 128},
    skeleton_keypoints=skeleton_keypoints,
    view="side",
    direction="south",
    init_images=[pil_image],
    init_image_strength=300,
    reference_image=pil_image,
    inpainting_images=[pil_image],

)

frames = [img.pil_image() for img in animation_response.images]
frames[0].save("dragon_idle.gif", save_all=True, append_images=frames[1:], duration=150, loop=0)
frames[0].show()