# Generated by Django 3.1.6 on 2021-02-06 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="car",
            name="rate",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="car",
            name="votes",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
