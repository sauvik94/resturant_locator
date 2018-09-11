from rest_framework import serializers

from .models import Resturant,Coordinate
from rest_framework.serializers import ModelSerializer

class CoordinateSerializer(ModelSerializer):
    class Meta:
        model = Coordinate
        fields = ('coordinate_id', 'latitude', 'longitude')


class ResturantSerializer(ModelSerializer):
    coordinate = serializers.SlugRelatedField('coordinate_id', queryset=Coordinate.objects.all())
    class Meta:
        model = Resturant
        fields = ('resturant_id', 'resturant_name', 'coordinate')


class ResturantDisplaySerializer(ModelSerializer):
    coordinate = CoordinateSerializer(many=False,required=True)
    class Meta:
        model = Resturant
        fields =  '__all__'


