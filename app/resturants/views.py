from _decimal import Decimal
from cmath import sqrt

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.resturants.data.data import resturant_list
from app.resturants.models import Coordinate, Resturant
from app.resturants.serializers import CoordinateSerializer, ResturantSerializer, ResturantDisplaySerializer
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
            coordinate_serilizer_data = { 'latitude':latitude, 'longitude' : longitude }
            coordinate_serilizer = CoordinateSerializer(data=coordinate_serilizer_data)
            if coordinate_serilizer.is_valid():
                coordinate = coordinate_serilizer.save()
            else:
                return Response({'status': constants.API_ERROR, 'message': coordinate_serilizer.errors},
                                status=status.HTTP_400_BAD_REQUEST)
        try:
            Resturant.objects.get(resturant_name=name, coordinate=coordinate)
        except Resturant.DoesNotExist:
            resturant_serilizer_data = {'resturant_name': name, 'coordinate': coordinate.coordinate_id}
            resturant_serilizer = ResturantSerializer(data=resturant_serilizer_data)
            if resturant_serilizer.is_valid():
                resturant_serilizer.save()
            else:
                return Response({'status': constants.API_ERROR, 'message': resturant_serilizer_data.errors},
                                status=status.HTTP_400_BAD_REQUEST)
    return Response({'status': constants.API_SUCCESS, 'message' : 'resturant database created'},status = status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def resturant_locator(request):
    data = request.data
    latitude = Decimal(data['latitude'])
    longitude = Decimal(data['longitude'])
    coordinates = Coordinate.objects.filter(latitude__gte=(latitude-5),latitude__lte=(latitude+5), longitude__gte=longitude-5,
                                            longitude__lte=longitude+5)
    coordinate_list = []
    for coordinate in coordinates:
        a = sqrt(abs((latitude-coordinate.latitude)**2) + abs((longitude-coordinate.longitude)**2))
        print(a)
        print(type(a))
        if sqrt(abs((latitude-coordinate.latitude)**2) + abs((longitude-coordinate.longitude)**2)) <= Decimal(5):
            coordinate_list.append(coordinate.coordinate_id)
    if len(coordinate_list) == 0:
        return Response({'status': constants.API_ERROR, 'message': 'No resturant found'},
                        status=status.HTTP_204_NO_CONTENT)
    resturants = Resturant.objects.filter(coordinate_id__in = coordinate_list)

    return Response({'status': constants.API_SUCCESS, 'message': 'Resturant found', 'data' : ResturantDisplaySerializer(resturants,
                                                                                                                 many=True).data},
                    status=status.HTTP_200_OK)

