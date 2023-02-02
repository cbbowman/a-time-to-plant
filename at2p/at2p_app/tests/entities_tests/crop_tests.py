from django.test import TestCase
from at2p_app.domain.entities.crop import Crop, CropError
from at2p_app.domain.value_objects.temperature import TempRange


class TestCrop(TestCase):
    def setUp(self) -> None:
        self.crop = Crop(
            id=73,
            name="Boberries",
            abs_range=TempRange.new(40, 80),
            opt_range=TempRange.new(65, 75),
        )
        return super().setUp()

    def test_create_from_dict(self):
        initdict = {
            "name": "Boberries",
            "abs_range": TempRange.new(40, 80),
            "opt_range": TempRange.new(65, 75),
        }
        c = Crop.from_dict(initdict)
        self.assertTrue(isinstance(c, Crop))

    def test_crop_creation(self):
        self.assertTrue(isinstance(self.crop, Crop))

    def test_str(self) -> None:
        self.assertEqual(
            self.crop.__str__(), f"{self.crop.name}"
        )

    def test_validation(self):
        initdict = {
            "name": "",
            "abs_range": TempRange.new(40, 80),
            "opt_range": TempRange.new(65, 75),
        }
        self.assertRaises(CropError, Crop.from_dict, initdict)

        initdict = {
            "name": 12,
            "abs_range": TempRange.new(40, 80),
            "opt_range": TempRange.new(65, 75),
        }
        self.assertRaises(CropError, Crop.from_dict, initdict)
