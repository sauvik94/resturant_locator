from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.resturants.data.data import resturant_list
from app.resturants.models import Coordinate, Resturant
from app.resturants.serializers import CoordinateSerializer, ResturantSerializer, ResturantDisplaySerializer
from common.authentication.authentication import JWTAuthentication
from common.util import is_missing_param_in_request
from constants import constants
from constants.api_mandatory_field_lists import APIMandatoryFieldList


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
            resturant_serializer_data = {'resturant_name': name, 'coordinate': coordinate.coordinate_id}
            resturant_serializer = ResturantSerializer(data=resturant_serializer_data)
            if resturant_serializer.is_valid():
                resturant_serializer.save()
            else:
                return Response({'status': constants.API_ERROR, 'message': resturant_serializer_data.errors},
                                status=status.HTTP_400_BAD_REQUEST)
    return Response({'status': constants.API_SUCCESS, 'message' : 'resturant database created'},status = status.HTTP_201_CREATED)


def is_valid_resturant_request(data):
    if data is None or not data:
        return False,"payload can not be empty"
    mandatory_fields = APIMandatoryFieldList.get_mandatory_field_list(key='resturant_locator')
    is_missing_param, message =  is_missing_param_in_request(dict=data, key_list=mandatory_fields)
    if is_missing_param:
        return False, message
    latitude = data['latitude']
    longitude = data['longitude']
    try:
        latitude = float(latitude)
    except ValueError:
        return False, "latitude and longitude are float fields, format should be latitude : 00.0 and longitude : 00.0"
    try:
        longitude = float(longitude)
    except ValueError:
        return False, "latitude and longitude are float fields, format should be latitude : 00.0 and longitude : 00.0"
    if latitude > 180 or latitude < -180:
        return False, "latitude should be in range -180 to 180"
    if longitude > 180 or longitude < -180:
        return False, "longitude should be in range -180 to 180"

    return True, None


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def resturant_locator(request):
    data = request.data
    is_valid_request, message = is_valid_resturant_request(data=data)
    if not is_valid_request:
        return Response({'status': constants.API_ERROR, 'message': message}, status=status.HTTP_400_BAD_REQUEST)

    latitude = float(data['latitude'])
    longitude = float(data['longitude'])
    coordinates = Coordinate.objects.filter(latitude__gte=(latitude-5),latitude__lte=(latitude+5), longitude__gte=longitude-5,
                                            longitude__lte=longitude+5)
    coordinate_list = []
    for coordinate in coordinates:
        a = abs((abs(latitude-coordinate.latitude)**2) + abs(abs(longitude-coordinate.longitude)**2))
        if (a**0.5) <= float(5):
            coordinate_list.append(coordinate.coordinate_id)
    if len(coordinate_list) == 0:
        return Response({'status': constants.API_ERROR, 'message': 'No resturant found'},
                        status=status.HTTP_204_NO_CONTENT)
    resturants = Resturant.objects.filter(coordinate_id__in = coordinate_list)

    if 2>len((coordinate_list))>0:
        message = " {0} Restaurant found".format(len(coordinate_list))
    else:
        message = " {0} Restaurants found".format(len(coordinate_list))

    return Response({'status': constants.API_SUCCESS, 'message': message, 'data' : ResturantDisplaySerializer(resturants,
                                                                                                                 many=True).data},
                    status=status.HTTP_200_OK)

