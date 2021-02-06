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

    def test_get_cars_view_returns_list(self):
        response = self.client.get(self.url)

        self.assertEqual(type(response.data), list)

    def test_view_returns_expected_number_of_objects(self):
        Car.objects.create(make='Volvo', model='V40')

        response = self.client.get(self.url)

        self.assertEqual(len(response.data), 1)

    def test_view_returns_data_with_expected_format(self):
        Car.objects.create(make='Volvo', model='V40')
        expected_keys = ['make', 'model']
        response = self.client.get(self.url)

        for key in response.data[0].keys():
            self.assertIn(key, expected_keys)

    def test_view_handles_returning_multiple_objects(self):
        Car.objects.create(make='Volvo', model='V40')
        Car.objects.create(make='Fiat', model='Uno')
        Car.objects.create(make='X-wing', model='Fighter')

        response = self.client.get(self.url)

        self.assertEqual(len(response.data), 3)
