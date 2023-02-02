from django.test import TestCase
from at2p_app.domain.entities.place import Place
from at2p_app.domain.value_objects.location import ZipCode
from at2p_app.domain.entities.planter import Planter, PlanterError


class TestPlanter(TestCase):
    def setUp(self) -> None:
        self.username = "MarkPugner"
        self.location = Place.new(ZipCode.new("22401"))
        self.planter = Planter.new(username=self.username, location=self.location)
        return super().setUp()

    def test_creation(self):
        self.assertIsInstance(self.planter, Planter)
        self.assertEqual(self.planter.username, self.username)
        self.assertEqual(self.planter.location, self.location)
        self.assertIsInstance(self.planter.id, int)
        self.assertIsInstance(self.planter.crops, list)

    def test_validation_username(self):
        new_username = 1234
        self.assertRaises(PlanterError, self.planter.change_username, new_username)

    def test_validation_location(self):
        new_location = "22405"
        self.assertRaises(PlanterError, self.planter.change_location, new_location)
