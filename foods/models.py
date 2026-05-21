from django.db import models

class Food(models.Model):
    FOOD_TYPE_CHOICES = [
        ('new', 'Yangi ovqat'),
        ('leftover', 'Qolgan ovqat'),
    ]

    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='foods')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Narx turi siz yozgandek CharField holida qoldi (belgilar qo'shish uchun)
    price = models.CharField(max_length=50)
    image = models.ImageField(upload_to='foods/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    
    # 📌 YANGI TIZIM UCHUN QO'SHILGAN MAYDONLAR
    food_type = models.CharField(max_length=10, choices=FOOD_TYPE_CHOICES, default='new')
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"