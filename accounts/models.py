import imp
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import uuid


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    speciality = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
