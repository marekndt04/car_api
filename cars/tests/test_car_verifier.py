from unittest import TestCase
from unittest.mock import patch

from cars.car_verifier import fetch_cars_by_make
from cars.car_verifier import validate_car_exists
from cars.car_verifier import verify_car


class TestCarVerifier(TestCase):

    def test_car_verifier_raise_error_with_bad_car(self):
        bad_car = {'make': 'not', 'model': 'a car'}

        with self.assertRaises(Exception):
            verify_car(make=bad_car['make'], model=bad_car['model'])

    @patch('cars.car_verifier.fetch_cars_by_make')
    def test_car_verifier_calls_fetch_cars_function(self, mock_fetch):
        good_car = {'make': 'Honda', 'model': 'Accord'}

        verify_car(make=good_car['make'], model=good_car['model'])
        self.assertTrue(mock_fetch.called)

    @patch('cars.car_verifier.validate_car_exists')
    def test_car_verifier_calls_validate_car_exists_function(self, mock_validate):
        good_car = {'make': 'Honda', 'model': 'Accord'}

        verify_car(make=good_car['make'], model=good_car['model'])
        self.assertTrue(mock_validate.called)
