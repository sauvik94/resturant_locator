class APIMandatoryFieldList(object):
    field_list = {
        'signup': ['first_name','last_name','email', 'password'],
        'login': ['email', 'password'],
        'resturant_locator' :['latitude', 'longitude'],
    }

    @staticmethod
    def get_mandatory_field_list(key):
        try:
            return APIMandatoryFieldList.field_list[key]
        except AttributeError:
            return None
