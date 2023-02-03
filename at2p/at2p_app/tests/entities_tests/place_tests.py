from django.test import TestCase
from at2p_app.domain.entities.place import Place, PlaceError
from at2p_app.domain.value_objects.location import ZipCode


class PlaceTest(TestCase):
    def setUp(self) -> None:
        self.zip = ZipCode.new("22407")
        self.place = Place.new(self.zip)
        return super().setUp()

    def test_create_place(self) -> None:
        p_str = f"{self.place.zip_code}, {self.place.country.code}"
        self.assertIsInstance(self.place, Place)
        self.assertEqual(self.place.__str__(), p_str)
        self.assertEqual(self.place.__repr__(), p_str)
        return

    def test_validation(self) -> None:
        bad_value = 12
        self.assertRaises(PlaceError, Place.new, zip_code=bad_value)
        bad_value = "GR"
        self.assertRaises(PlaceError, Place.new, zip_code=self.zip, country=bad_value)
