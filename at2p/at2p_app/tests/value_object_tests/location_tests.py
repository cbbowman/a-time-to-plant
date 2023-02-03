from django.test import TestCase
from at2p_app.domain.common.error import CountryError, ZipCodeError
from at2p_app.domain.value_objects.location import ZipCode, Country


class CountryTest(TestCase):
    def setUp(self) -> None:
        self.code = "US"
        self.country = Country.new(code=self.code)
        self.name = self.country.name
        return super().setUp()

    def test_create_country(self) -> None:
        self.assertTrue(isinstance(self.country, Country))

    def test_str(self):
        self.assertEqual(self.country.__str__(), self.name)

    def test_code_isnt_a_str(self) -> None:
        code = 42
        self.assertRaises(CountryError, Country.new, code=code)

    def test_code_wrong_length(self):
        code = "GRE"
        self.assertRaises(CountryError, Country.new, code=code)

    def test_code_unsupported(self):
        code = "GR"
        self.assertRaises(CountryError, Country.new, code=code)

    def test_cleaning(self):
        code = " U s  \n"
        c = Country.new(code)
        self.assertEqual(c.code, "US")


class ZipCodeTest(TestCase):
    def setUp(self) -> None:
        self.zip = ZipCode.new("22405")
        return super().setUp()

    def test_create_zip(self) -> None:
        self.assertTrue(isinstance(self.zip, ZipCode))

    def test_str(self):
        self.assertEqual(self.zip.__str__(), self.zip.zip)
        self.assertEqual(self.zip.__repr__(), self.zip.zip)

    def test_code_isnt_a_str(self) -> None:
        code = 42
        self.assertRaises(ZipCodeError, ZipCode.new, code)
