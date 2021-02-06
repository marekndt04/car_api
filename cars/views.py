from rest_framework.response import Response
from rest_framework.views import APIView

from cars.models import Car


class GetCarsView(APIView):

    def get(self, request):
        cars = []
        for car in Car.objects.all():
            cars.append({
                'make': car.make,
                'model': car.model,
            })

        return Response(cars)
