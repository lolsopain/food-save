from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255, verbose_name="Restoran nomi")
    address = models.CharField(max_length=255, verbose_name="Manzili")
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name