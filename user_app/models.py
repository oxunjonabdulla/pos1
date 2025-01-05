from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator

from .manager import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=455, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    role = models.CharField(max_length=455, null=True, blank=True)
    image = models.ImageField(upload_to='users', null=True, blank=True)
    location = models.CharField(max_length=455, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    password = models.CharField(max_length=128, validators=[MinLengthValidator(4)])

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Foydalanuvchilar"