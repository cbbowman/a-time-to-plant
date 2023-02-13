from unittest import TestCase
from at2p_app.domain.common.error import InterfaceError
from at2p_app.domain.entities.place import Place
from at2p_app.domain.use_cases.place_interface import PlaceInterface
from at2p_app.adapters.repositories.place_repo import TestingPlaceRepo


class TestPlaceInterface(TestCase):
    def setUp(self) -> None:
        self.zip_code = "22407"
        self.place = Place.new(self.zip_code)
        self.repo = TestingPlaceRepo()
        self.interface = PlaceInterface.new(self.repo)
        return super().setUp()

    def test_instantiation(self):
        self.assertIsInstance(self.interface, PlaceInterface)

    def test_create_a_place(self):
        place = self.interface.create_place(self.zip_code)
        self.assertIsInstance(place, Place)

    def test_get_a_place(self):
        place = self.interface.get_place(self.place.id)
        self.assertIsInstance(place, Place)

    def test_save_a_place(self):
        self.assertIsNone(self.interface.save_place(self.place))

    def test_delete_a_place(self):
        self.assertIsNone(self.interface.delete_place(self.place))

    def test_validation(self):
        self.assertRaises(InterfaceError, PlaceInterface.new, "not a repo")
