from rest_framework.generics import ListCreateAPIView
from rest_framework.renderers import JSONRenderer

from cars.models import Car
from cars.serializers import CarSerializer


class GetCarsView(ListCreateAPIView):
    renderer_classes = [JSONRenderer]

    queryset = Car.objects.all()
    serializer_class = CarSerializer
