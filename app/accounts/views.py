from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.accounts.models import User
from app.accounts.serializers import UserSerializer
from common.util import is_missing_param_in_request, is_empty
from constants import constants
from constants.api_mandatory_field_lists import APIMandatoryFieldList

def is_valid_signup_request(data):
    if data is None or not data:
        return False, 'payload cannot be empty'

    mandatory_fields = APIMandatoryFieldList.get_mandatory_field_list(key='signup')
    is_missing_mandatory_details, message = is_missing_param_in_request(dict=data, key_list=mandatory_fields)
    if is_missing_mandatory_details:
        return False, message

    email = data['email']
    try:
        user = User.objects.get(email=email)
        return False, 'Given Email ID {0} is already registered'.format(email)
    except User.DoesNotExist:
        pass

    return True, None

def update_user(data):
    try:
        user = User.objects.get(email=data['email'])
    except User.DoesNotExist:
        user = User.objects.create(email=data['email'])

    user_serializer_data = {
        'first_name': data['email'] if not is_empty(dict=data, key='first_name') else user.first_name,
        'last_name': data['last_name'] if not is_empty(dict=data, key='last_name') else user.last_name,
        'email': data['email'] if not is_empty(dict=data, key='email') else user.email,
        'password': data['password'] if not is_empty(dict=data, key='password') else user.password,
    }
    user_serializer = UserSerializer(user, data = user_serializer_data)
    if user_serializer.is_valid():
        user_serializer.save()
        return  True, None
    else:
        return False, user_serializer.errors

@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes([])
def signup(request):
    """
    {
        "email": "emailone@yopmail.com",
        "password": "password_ONE"
    }
    """
    data = request.data
    is_valid_request, message = is_valid_signup_request(data=data)
    if not is_valid_request:
        return Response({'status': constants.API_ERROR, 'message': message}, status=status.HTTP_400_BAD_REQUEST)

    is_success, message = update_user(data=data)
    if not is_success:
        return Response({'status': constants.API_ERROR, 'message': message},
                        status=status.HTTP_400_BAD_REQUEST)

    return Response({'status': constants.API_SUCCESS, 'message': 'Successfully registered new user'},
                    status=status.HTTP_201_CREATED)

