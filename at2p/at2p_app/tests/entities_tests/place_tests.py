from django.test import TestCase
from at2p_app.domain.entities.place import Place, PlaceError
from at2p_app.domain.value_objects.location import ZipCode


class PlaceTest(TestCase):
    def setUp(self) -> None:
        self.zip = ZipCode.new("22407")
        self.place = Place(zip=self.zip)
        return super().setUp()

    def test_create_place(self) -> None:
        p_str = f"{self.place.zip}, {self.place.country}"
        self.assertIsInstance(self.place, Place)
        self.assertEqual(self.place.__str__(), p_str)
        return

    def test_validation(self) -> None:
        bad_value = 12
        self.assertRaises(PlaceError, Place, zip=bad_value)
        bad_value = "GR"
        self.assertRaises(PlaceError, Place, zip=self.zip, country=bad_value)
        self.assertRaises(PlaceError, Place, zip=self.zip, crops=bad_value)
        self.assertRaises(PlaceError, Place, zip=self.zip, crops=[bad_value])
        self.assertRaises(PlaceError, Place, zip=self.zip, weather=bad_value)
