import http
from unittest.mock import patch

from django.test import TestCase
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APIClient

from cars.car_verifier import ObjectNotExistsException
from cars.models import Car


class TestGetCarsView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse_lazy('get-cars')

    def test_get_cars_returns_list_of_http_ok_response(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_get_cars_view_returns_empty_list_without_objects(self):
        response = self.client.get(self.url)

        self.assertEqual(response.data, [])

    def test_view_returns_data_with_expected_format(self):
        Car.objects.create(make='Volvo', model='V40')
        expected_keys = ['make', 'model', 'rate', 'votes']
        response = self.client.get(self.url)

        for key in response.data[0].keys():
            self.assertIn(key, expected_keys)

    def test_view_returns_expected_output(self):
        car = Car.objects.create(make='Volvo', model='V40')

        response = self.client.get(self.url)
        expected_output = [
            {
                'make': car.make,
                'model': car.model,
                'rate': car.rate,
                'votes': car.votes,
            }
        ]
        self.assertEqual(response.data, expected_output)

    def test_view_handles_returning_multiple_objects(self):
        Car.objects.create(make='Volvo', model='V40')
        Car.objects.create(make='Fiat', model='Uno')
        Car.objects.create(make='X-wing', model='Fighter')

        response = self.client.get(self.url)

        self.assertEqual(len(response.data), 3)


class TestPostCarsView(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse_lazy('get-cars')

    @patch('cars.views.verify_car')
    def test_post_cars_view_can_save_car_object(self, mock_verify):
        mock_verify.return_value = True
        response = self.client.post(self.url, {'make': 'Reno', 'model': 'Laguna'})

        expected_car = Car.objects.get(make='Reno')

        self.assertEqual(expected_car.make, 'Reno')
        self.assertEqual(response.status_code, http.HTTPStatus.CREATED)

    @patch('cars.views.verify_car')
    def test_post_cars_view_returns_error_with_duplicated_data(self, mock_verify):
        mock_verify.return_value = True
        car = Car.objects.create(make='BMW', model='320')

        response = self.client.post(self.url, {'make': car.make, 'model': car.model})

        self.assertEqual(response.status_code, http.HTTPStatus.CONFLICT)

    @patch('cars.views.verify_car')
    def test_cars_view_validates_bad_request_data_and_raise_error(self, mock_verify):
        mock_verify.return_value = True
        response = self.client.post(self.url, {'some': 'strange_data'})

        self.assertEqual(response.status_code, http.HTTPStatus.BAD_REQUEST)

    @patch('cars.views.verify_car')
    def test_post_cars_returns_error_with_bad_car(self, mock_verify):
        mock_verify.side_effect = ObjectNotExistsException

        response = self.client.post(self.url, {'make': 'Volvo', 'model':'V40'})

        self.assertEqual(response.status_code, http.HTTPStatus.BAD_REQUEST)


class TestRateCarView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse_lazy('rate-car')

    def test_view_return_error_with_non_number_rate(self):
        response = self.client.post(
            self.url, {'make': 'make', 'model': 'model', 'rate': 'string :O'}
        )

        self.assertEqual(response.status_code, http.HTTPStatus.BAD_REQUEST)

    def test_view_returns_error_with_bad_request_structure(self):
        response = self.client.post(
            self.url, {'again': 'something', 'went': 'wrong'}
        )

        self.assertEqual(response.status_code, http.HTTPStatus.BAD_REQUEST)

    def test_view_returns_error_with_not_existing_car(self):
        response = self.client.post(
            self.url, {'make': 'do we ', 'model': 'have that ?', 'rate': 1}
        )

        self.assertEqual(response.status_code, http.HTTPStatus.BAD_REQUEST)

    def test_view_returns_error_with_rate_out_of_scale(self):
        car = Car.objects.create(make='Lada', model='Samara')
        response = self.client.post(
            self.url, {'make': car.make, 'model': car.model, 'rate': 6}
        )

        self.assertEqual(response.status_code, http.HTTPStatus.BAD_REQUEST)

    def test_view_saves_rate_properly(self):
        car = Car.objects.create(make='Horse', model='Roach', rate=4, votes=1)
        self.client.post(
            self.url, {'make': car.make, 'model': car.model, 'rate': 5}
        )

        car.refresh_from_db()

        self.assertEqual(car.rate, 4.5)

    def test_view_saves_votes_properly(self):
        car = Car.objects.create(make='Lada', model='Samara', rate=12, votes=3)
        self.client.post(
            self.url, {'make': car.make, 'model': car.model, 'rate': 4}
        )

        car.refresh_from_db()

        self.assertEqual(car.votes, 4)


class TestPopularCarsView(TestCase):

    def test_popular_view_returns_expected_output(self):
        one = Car.objects.create(make='one', model='1', rate=3, votes=1)
        two = Car.objects.create(make='two', model='2', rate=4, votes=2)
        three = Car.objects.create(make='three', model='3', rate=5, votes=3)

        url = reverse_lazy('popular')
        response = self.client.get(url)

        expected_output = [
            {
                'make': one.make,
                'model': one.model,
                'rate': one.rate,
                'votes': one.votes,
            },
            {
                'make': two.make,
                'model': two.model,
                'rate': two.rate,
                'votes': two.votes,
            },
            {
                'make': three.make,
                'model': three.model,
                'rate': three.rate,
                'votes': three.votes,
            },
        ]

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(response.data, expected_output)