from unittest import TestCase

from cars.models import Car
from cars.serializers import CarSerializer


class TestCarSerializer(TestCase):
    def setUp(self) -> None:
        self.car = Car.objects.create(make='Reno', model='Laguna')

    def test_serializer_returns_expected_output(self):
        serializer = CarSerializer(self.car)
        expected_body = {
            'make': 'Reno',
            'model': 'Laguna',
            'rate': 0,
            'votes': 0,
        }
        self.assertEqual(expected_body, serializer.data)
