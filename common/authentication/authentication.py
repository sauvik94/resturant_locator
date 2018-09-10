import jwt
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

from app.accounts.models import User

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_userid_from_payload = api_settings.JWT_PAYLOAD_GET_USER_ID_HANDLER


class JWTAuthentication(JSONWebTokenAuthentication):
    def authenticate(self, request):
        try:
            val = super(JWTAuthentication, self).authenticate(request)
            if val is None:
                message = _('Unauthorized access')
                raise exceptions.PermissionDenied(message)
            user, jwt_value = val
            return user, jwt_value
        except jwt.ExpiredSignature:
            message = _('JWT has expired.')
            raise exceptions.AuthenticationFailed(message)

    def authenticate_credentials(self, payload):
        user_id = jwt_get_userid_from_payload(payload)
        user = User.objects.get(user_id=user_id)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)

        return user
