import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError


class ObjectNotExistsException(Exception):
    pass


def verify_car(make, model):
    cars = fetch_cars_by_make(make)
    try:
        validate_car_exists(make, model, cars)
    except ValidationError:
        raise ObjectNotExistsException


def fetch_cars_by_make(make):
    url = settings.CAR_API_DATABASE_ENDPOINT + make.lower() + '?format=json'
    cars = requests.get(url).json()
    return cars['Results']


def validate_car_exists(make, model, fetched_cars):
    for car in fetched_cars:
        fetched_make = car['Make_Name'].lower()
        fetched_model = car['Model_Name'].lower()
        if make.lower() == fetched_make and model.lower() == fetched_model:
            return True
    raise ValidationError
