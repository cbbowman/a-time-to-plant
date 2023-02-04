from django.test import TestCase
from at2p_app.domain.entities.place import Place


class PlaceTest(TestCase):
    def setUp(self) -> None:
        self.place = Place.new("22407", "US")
        return super().setUp()

    def test_create_place(self) -> None:
        p_str = f"{self.place.zip_code}, {self.place.country.code}"
        self.assertIsInstance(self.place, Place)
        self.assertEqual(self.place.__str__(), p_str)
        self.assertEqual(self.place.__repr__(), p_str)
        return
