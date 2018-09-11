import uuid
from _decimal import Decimal
from django.db import models

class Coordinate(models.Model):
    coordinate_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)


class Resturant(models.Model):
    resturant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resturant_name = models.CharField(blank=False,max_length=200)
    coordinate = models.ForeignKey(Coordinate,on_delete=models.CASCADE)