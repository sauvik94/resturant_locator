from .models import User
from rest_framework.serializers import ModelSerializer
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id','first_name','last_name','email','password')
