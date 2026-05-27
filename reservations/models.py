from django.db import models

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    food = models.ForeignKey('foods.Food', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True)
    client_name = models.CharField(max_length=255, blank=True, null=True)
    client_phone = models.CharField(max_length=30, blank=True, null=True)
    delivery_type = models.CharField(max_length=30)
    payment_method = models.CharField(max_length=30)
    latitude = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.client_name}"