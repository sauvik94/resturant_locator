import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.core import validators
from django.utils import timezone

class User(AbstractBaseUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField(max_length=50, unique=True,
                              validators=[validators.EmailValidator(message='Provide a valid email')])
    username = models.EmailField(max_length=50, blank=True, null=True, unique=True,
                                 validators=[validators.EmailValidator(message='Provide a valid email')])
    password = models.CharField(max_length = 100)
    jwt_secret = models.UUIDField(default=uuid.uuid4, editable=False)

    USERNAME_FIELD = 'username'

def jwt_get_secret_key(self_model):
    return self_model.jwt_secret