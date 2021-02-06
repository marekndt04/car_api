from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer

from cars.models import Car
from cars.serializers import CarSerializer


class GetCarsView(ListAPIView):
    renderer_classes = [JSONRenderer]

    queryset = Car.objects.all()
    serializer_class = CarSerializer
