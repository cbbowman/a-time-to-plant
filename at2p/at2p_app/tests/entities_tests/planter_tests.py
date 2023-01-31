from django.test import TestCase
from at2p_app.domain.entities.location import Place
from at2p_app.domain.entities.planter import Planter, PlanterError


class TestPlanter(TestCase):
    def setUp(self) -> None:
        self.id = 73
        self.username = "MarkPugner"
        self.location = Place(zip="22401")
        self.planter = Planter(username=self.username, location=self.location)
        return super().setUp()

    def test_creation(self):
        self.assertIsInstance(self.planter, Planter)
        self.assertEqual(self.planter.username, self.username)
        self.assertEqual(self.planter.location, self.location)
        self.assertIsInstance(self.planter.id, int)
        self.assertIsInstance(self.planter.crops, list)

    def test_validation_username(self):
        new_username = 1234
        self.planter.username = new_username
        self.assertRaises(PlanterError, self.planter._validate)

    def test_validation_location(self):
        new_location = "22405"
        self.planter.location = new_location
        self.assertRaises(PlanterError, self.planter._validate)

    def test_validation_crops(self):
        new_crops = "22405"
        self.planter.crops = new_crops
        self.assertRaises(PlanterError, self.planter._validate)

    def test_validation_id(self):
        new_id = "22405"
        self.planter.id = new_id
        self.assertRaises(PlanterError, self.planter._validate)
