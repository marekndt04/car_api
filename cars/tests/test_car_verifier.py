from unittest import TestCase
from unittest.mock import patch

from cars.car_verifier import verify_car


class TestCarVerifier(TestCase):

    def test_car_verifier_raise_error_with_bad_car(self):
        bad_car = {'make': 'not', 'model': 'a car'}

        with self.assertRaises(Exception):
            verify_car(make=bad_car['make'], model=bad_car['model'])

    @patch('cars.car_verifier.request')
    def test_car_verifier_calls_request_function(self, mock_request):
        good_car = {'make': 'Honda', 'model': 'Accord'}

        verify_car(make=good_car['make'], model=good_car['model'])
        self.assertTrue(mock_request.called)

