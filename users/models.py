from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    USER_ROLES = (
        ('client', 'Client'),
        ('owner', 'Restaurant Owner'),
    )

    role = models.CharField(max_length=10, choices=USER_ROLES, default='client')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email