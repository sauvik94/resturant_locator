import uuid
from _decimal import Decimal
from django.db import models

class Coordinate(models.Model):
    coordinate_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    latitude = models.DecimalField(max_digits=20,decimal_places=10,default=Decimal('0.0000'))
    longitude = models.DecimalField(max_digits=20, decimal_places=10, default=Decimal('0.0000'))


class Resturant(models.Model):
    resturant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resturant_name = models.CharField(blank=False,max_length=200)
    coordinate = models.ForeignKey(Coordinate,on_delete=models.CASCADE)