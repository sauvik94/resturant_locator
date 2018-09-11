from uuid import UUID

from django.contrib.auth.models import AnonymousUser
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def is_empty_array(arr):
    flag = True
    for curr_item in arr:
        if type(curr_item) is list:
            flag = is_empty_array(curr_item)
        elif curr_item is not None and curr_item != '' or curr_item != {}:
            flag = False
    return flag

def is_empty(dict, key):
    if not dict.__contains__(key):
        return True
    val = dict.get(key)
    if val is None or val == {} or val == '':
        return True
    if type(val) is list:
        return is_empty_array(val)
    if type(val) is dict:
        return not val
    return False


def is_empty_str(val):
    return val is None or val == ''


def is_missing_param_in_request(dict, key_list):
    missing_keys = []
    for curr_key in key_list:
        if is_empty(dict, curr_key):
            missing_keys.append(curr_key)
    if len(missing_keys) > 0:
        return True, 'Mandatory parameters missing in request : %s' % ', '.join(missing_keys)
    return False, None


def get_jwt_payload(request, user):
    payload = jwt_payload_handler(user)
    return payload


def get_jwt(request, user):
    payload = get_jwt_payload(request=request, user=user)
    return jwt_encode_handler(payload)


    return True, None