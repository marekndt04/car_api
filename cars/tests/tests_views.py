import http
from django.test import TestCase
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APIClient

from cars.models import Car


class TestGetCarsView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse_lazy('get-cars')

    def test_get_cars_return_list_of_http_ok_response(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_get_cars_view_returns_empty_list_without_objects(self):
        response = self.client.get(self.url)

        self.assertEqual(response.data, [])

    def test_view_returns_data_with_expected_format(self):
        Car.objects.create(make='Volvo', model='V40')
        expected_keys = ['make', 'model']
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

    def test_post_cars_view_can_save_car_object(self):
        self.client.post(self.url, {'make': 'Reno', 'model': 'Laguna'})

        expected_car = Car.objects.get(make='Reno')

        self.assertEqual(expected_car.make, 'Reno')

    def test_post_cars_view_returns_error_with_duplicated_data(self):
        car = Car.objects.create(make='BMW', model='320')

        response = self.client.post(self.url, {'make': car.make, 'model': car.model})

        self.assertEqual(response.status_code, http.HTTPStatus.CONFLICT)

    def test_cars_view_validates_bad_request_data_and_raise_error(self):
        response = self.client.post(self.url, {'some': 'strange_data'})

        self.assertEqual(response.status_code, http.HTTPStatus.BAD_REQUEST)
