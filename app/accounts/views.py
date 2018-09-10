import uuid
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from app.accounts.models import User
from app.accounts.serializers import UserSerializer
from common.authentication.authentication import JWTAuthentication
from common.util import is_missing_param_in_request, is_empty, get_jwt
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
        'first_name': data['first_name'] if not is_empty(dict=data, key='first_name') else user.first_name,
        'last_name': data['last_name'] if not is_empty(dict=data, key='last_name') else user.last_name,
        'email': data['email'] if not is_empty(dict=data, key='email') else user.email,
        'username': data['email'] if not is_empty(dict=data, key='email') else user.username,
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


def is_valid_login_request(data):
    if data is None or not data:
        return False,"payload can not be empty"
    mandatory_fields = APIMandatoryFieldList.get_mandatory_field_list(key='login')
    is_missing_param, message =  is_missing_param_in_request(dict=data, key_list=mandatory_fields)
    if is_missing_param:
        return False, message
    email = data['email']
    try:
        user = User.objects.get(email=email)
        if data['password'] != user.password:
            return False, "Wrong credentials given"
    except User.DoesNotExist:
        return False, "The email {0} is not registered yet".format(email)
    return  True, None


@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes([])
def login(request):
    data = request.data
    is_valid_request, message = is_valid_login_request(data=data)
    print(is_valid_request)
    if not is_valid_request:
        return  Response({'status': constants.API_ERROR, 'message' : message}, status = status.HTTP_400_BAD_REQUEST)

    user = User.objects.get(email=data['email'])
    user.jwt_secret = uuid.uuid4()
    user.save()
    jwt = str(get_jwt(request=request, user=user))
    data = {'user_id': user.user_id, 'jwt': jwt}
    return Response({'status' : constants.API_SUCCESS, 'message' : 'logged in successfully', 'data':data}, status= status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def logout(request):
    user = request.user
    user.jwt_secret = uuid.uuid4()
    user.save()
    return Response({'status' : constants.API_SUCCESS, 'message': "logged out"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def test_auth(request):
    user = request.user
    return  Response({'status' : constants.API_SUCCESS, 'data': user.email}, status= status.HTTP_200_OK)