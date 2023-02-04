from django.test import TestCase
from at2p_app.adapters.repositories.place_repo import (
    DjangoPlaceRepo,
    PlaceRepo,
    PlaceRepoError,
)
from at2p_app.domain.entities.place import Place, ZipCode


class TestDjangoRepo(TestCase):
    def setUp(self) -> None:
        self.zip_str = "22407"
        self.repo = DjangoPlaceRepo()
        return super().setUp()

    def test_instantiation(self):
        self.assertIsInstance(self.repo, PlaceRepo)

    def test_create_place(self):
        self.assertIsInstance(self.repo.create(self.zip_str), Place)

    def test_get_place(self):
        created_place = self.repo.create(self.zip_str)
        retrieved_place = self.repo.get(created_place.id)
        self.assertEqual(retrieved_place.id, created_place.id)

    def test_save_place(self):
        created_place = self.repo.create(self.zip_str)
        new_zip = ZipCode.new("22407")
        created_place.zip_code = new_zip
        self.repo.save(created_place)
        retrieved_place = self.repo.get(created_place.id)
        self.assertEqual(retrieved_place.zip_code, new_zip)

    def test_delete_place(self):
        created_place = self.repo.create(self.zip_str)
        self.repo.delete(created_place)
        self.assertRaises(PlaceRepoError, self.repo.get, created_place.id)
        self.assertRaises(PlaceRepoError, self.repo.save, created_place)
        self.assertRaises(PlaceRepoError, self.repo.delete, created_place)
