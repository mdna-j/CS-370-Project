import unittest
from unittest.mock import patch, MagicMock
from petsystem.PetGen import make_pet
from unittest.mock import ANY


class TestMakePet(unittest.TestCase):

    @patch("petsystem.PetGen.pixellab.Client")
    def test_gen_baseimg(self, mock_client_class):
        mock_client = MagicMock()
        mock_pil_img = MagicMock()  # Mocked PIL image object with .save()

        # simulate .pil_image() -> mock_pil_img
        mock_img = MagicMock()
        mock_img.pil_image.return_value = mock_pil_img

        mock_client.generate_image_bitforge.return_value.image = mock_img
        mock_client_class.return_value = mock_client

        pet = make_pet()
        result = pet.gen_baseimg("cute red dragon")

        self.assertEqual(result, mock_pil_img)
        self.assertEqual(pet.petpic, mock_pil_img)
        mock_pil_img.save.assert_called_once_with(ANY)

    @patch("petsystem.PetGen.pixellab.Client")
    def test_gen_idle_postions(self, mock_client_class):
        mock_client = MagicMock()
        mock_client.estimate_skeleton.return_value.keypoints = [
            {"x": 5, "y": 10, "label": "head", "z_index": 2}
        ]
        mock_client_class.return_value = mock_client

        pet = make_pet()
        pet.petpic = "fake_image"
        result = pet.gen_idle_postions([10, -10])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0]["y"], 20)
        self.assertEqual(result[1][0]["y"], 0)

    @patch("petsystem.PetGen.pixellab.Client")
    def test_gen_animation_and_save_as_gif(self, mock_client_class):
        mock_anim = MagicMock()
        mock_anim.images = [
            MagicMock(pil_image=MagicMock(return_value=MagicMock())),
            MagicMock(pil_image=MagicMock(return_value=MagicMock()))
        ]

        mock_client = MagicMock()
        mock_client.animate_with_skeleton.return_value = mock_anim
        mock_client_class.return_value = mock_client

        pet = make_pet()
        pet.petpic = "mocked image"
        result = pet.Gen_animation([[], []])
        self.assertEqual(result, mock_anim)

        with patch.object(pet, "animatedpet", mock_anim):
            first_frame_mock = mock_anim.images[0].pil_image.return_value
            with patch.object(first_frame_mock, "save") as mock_save:
                pet.save_as_gif("test.gif")
                mock_save.assert_called_once()


if __name__ == "__main__":
    unittest.main()
