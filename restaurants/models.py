from django.db import models
from users.models import User

class Restaurant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants', null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name="Restoran nomi")
    address = models.CharField(max_length=255, verbose_name="Manzili")
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name