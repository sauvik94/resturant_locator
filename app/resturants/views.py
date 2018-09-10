from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.resturants.data.data import resturant_list
from app.resturants.models import Coordinate, Resturant
from constants import constants


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def load_data(request):
    for i in resturant_list :
        name = i[0]
        latitude = i[1]
        longitude = i[2]
        try:
            coordinate = Coordinate.objects.get(latitude=latitude, longitude=longitude)
        except Coordinate.DoesNotExist:
            coordinate = Coordinate.objects.create(latitude=latitude, longitude=longitude)
        try:
            Resturant.objects.get(resturant_name=name, coordinate=coordinate)
        except Resturant.DoesNotExist:
            Resturant.objects.create(resturant_name=name, coordinate=coordinate)
    return Response({'status': constants.API_SUCCESS, 'message' : 'resturant database created'},status = status.HTTP_201_CREATED)
