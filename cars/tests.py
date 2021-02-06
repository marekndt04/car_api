import http
from django.test import TestCase
from rest_framework.test import APIClient


class TestGetCarsView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_cars_return_list_of_http_ok_response(self):
        response = self.client.get('get-cars')

        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_get_cars_view_returns_list(self):
        response = self.client.get('get-cars')

        self.assertEqual(type(response.body), list)
