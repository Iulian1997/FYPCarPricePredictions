from django.db import models
from django.conf import settings

class Favourites(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    transmission = models.CharField(max_length=50)
    mileage = models.FloatField()
    tax = models.IntegerField()
    mpg = models.FloatField()
    engine_size = models.FloatField()
    price = models.FloatField()

    def __str__(self):
        return str(self.id)

        