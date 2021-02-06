from django.db import models


class Car(models.Model):
    make = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    rate = models.FloatField(blank=True, null=True)
    votes = models.IntegerField(blank=True, null=True)
