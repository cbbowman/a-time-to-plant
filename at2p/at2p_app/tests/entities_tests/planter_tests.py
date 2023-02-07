from unittest import TestCase
from at2p_app.domain.entities.place import Place
from at2p_app.domain.entities.crop import Crop
from at2p_app.domain.value_objects.location import ZipCode
from at2p_app.domain.value_objects.temperature import TempRange
from at2p_app.domain.entities.planter import Planter, PlanterError


class TestPlanter(TestCase):
    def setUp(self) -> None:
        self.username = "MarkPugner"
        self.location = Place.new(ZipCode.new("22401"))
        self.planter = Planter.new(
            username=self.username, location=self.location
        )
        return super().setUp()

    def test_creation(self):
        self.assertIsInstance(self.planter, Planter)
        self.assertEqual(self.planter.username, self.username)
        self.assertEqual(self.planter.location, self.location)
        self.assertIsInstance(self.planter.id, int)
        self.assertIsInstance(self.planter.crops, list)

    def test_str_repr(self):
        self.assertEqual(
            self.planter.__str__(), f"{self.planter.username} ({self.planter.id})"
        )
        self.assertEqual(
            self.planter.__repr__(), f"{self.planter.username} ({self.planter.id})"
        )

    def test_validation_username(self):
        new_username = 1234
        self.assertRaises(
            PlanterError, self.planter.change_username, new_username
        )

    def test_validation_location(self):
        new_location = "22405"
        self.assertRaises(
            PlanterError, self.planter.change_location, new_location
        )

    def test_change_username(self):
        new_username = "bob"
        self.planter.change_username(new_username)
        self.assertEqual(self.planter.username, new_username)

    def test_change_location(self):
        new_location = Place.new(ZipCode.new("22407"))
        self.planter.change_location(new_location)
        self.assertEqual(self.planter.location, new_location)

    def test_add_crop(self):
        self.crop = Crop.new(
            name="Boberries",
            abs_range=TempRange.new(40, 80),
            opt_range=TempRange.new(65, 75),
        )
        self.planter.add_crop(self.crop)
        self.assertIn(self.crop, self.planter.crops)
        self.assertRaises(PlanterError, self.planter.add_crop, self.crop)

    def test_remove_crop(self):
        self.crop = Crop.new(
            name="Boberries",
            abs_range=TempRange.new(40, 80),
            opt_range=TempRange.new(65, 75),
        )
        self.planter.add_crop(self.crop)
        self.planter.remove_crop(self.crop)
        self.assertNotIn(self.crop, self.planter.crops)
        self.assertFalse(self.planter._crop_in_list(self.crop))
        self.assertRaises(PlanterError, self.planter.remove_crop, self.crop)
