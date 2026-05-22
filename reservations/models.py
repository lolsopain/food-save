from django.db import models
from users.models import User
from foods.models import Food

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    # null=True, blank=True qilindi, chunki mehmonlar ham buyurtma bera olishi kerak
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservations',
        null=True,
        blank=True
    )
    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    reserved_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        user_email = self.user.email if self.user else "Mehmon"
        return f"{user_email} -> {self.food.name}"