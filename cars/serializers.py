from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, status
from rest_framework.serializers import ModelSerializer

from cars.models import Car


class CarSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = ['make', 'model']

    def create(self, validated_data):
        make = validated_data['make']
        model = validated_data['model']
        try:
            Car.objects.get(make=make, model=model)
        except ObjectDoesNotExist:
            Car.objects.create(**validated_data)

        object_exists_error = serializers.ValidationError('object already exists')
        object_exists_error.status_code = status.HTTP_409_CONFLICT
        raise object_exists_error

