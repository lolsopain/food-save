from django.db import models

class Food(models.Model):
    FOOD_TYPES = (
        ('new', 'New'),
        ('leftover', 'Leftover'),
    )
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='foods')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.CharField(max_length=50)
    image = models.ImageField(upload_to='foods/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    food_type = models.CharField(max_length=20, choices=FOOD_TYPES, default='new')
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return self.name