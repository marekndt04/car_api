from django.core.exceptions import ObjectDoesNotExist
from rest_framework import response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer

from cars.car_verifier import ObjectNotExistsException
from cars.car_verifier import verify_car
from cars.models import Car
from cars.serializers import CarSerializer


class GetCarsView(ListCreateAPIView):
    renderer_classes = [JSONRenderer]

    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def post(self, request, *args, **kwargs):
        try:
            verify_car(request.data['make'], request.data['model'])
        except ObjectNotExistsException:
            return response.Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=['such car does not exist']
            )
        except KeyError:
            return response.Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=['car should have make and model']
            )
        return super().post(request, *args, **kwargs)


class RateCarView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        car_data = request.data
        try:
            self.validate_request(car_data)
        except ValidationError:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            car = Car.objects.get(make=car_data['make'], model=car_data['model'])
        except ObjectDoesNotExist:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)

        car.votes += 1
        incremented_rate = int(car_data['rate']) + car.rate
        car.rate = incremented_rate / car.votes
        car.save()
        return response.Response(status=status.HTTP_201_CREATED)

    def validate_request(self, car_data):
        expected_keys = ['make', 'model', 'rate']
        try:
            for key in expected_keys:
                car_data[key]
        except KeyError:
            raise ValidationError
        try:
            int(car_data['rate'])
        except ValueError:
            raise ValidationError
        if int(car_data['rate']) not in range(1, 6):
            raise ValidationError


class PopularCarsView(ListAPIView):
    renderer_classes = [JSONRenderer]

    queryset = Car.objects.all().order_by('-votes')
    serializer_class = CarSerializer
