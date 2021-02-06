def verify_car(make, model):
    cars = fetch_cars_by_make(make)
    try:
        validate_car_exists(make, model, cars)
    except Exception:
        raise


def fetch_cars_by_make(make):
    pass


def validate_car_exists(make, model, cars):
    pass
