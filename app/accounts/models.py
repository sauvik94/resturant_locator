import uuid
from django.db import models
from django.core import validators
from django.utils import timezone

class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField(max_length=50, unique=True,
                              validators=[validators.EmailValidator(message='Provide a valid email')])
    password = models.CharField(max_length = 100)