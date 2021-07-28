import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": 5432,
    }
}
