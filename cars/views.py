from rest_framework import response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
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



