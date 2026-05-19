from django.db import models

class Food(models.Model):
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='foods')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # 1. Narxga ham raqam, ham harf va '$' belgilarini yozish uchun CharField-ga o'zgartirildi
    price = models.CharField(max_length=50)
    
    # 2. Taomga rasm yuklash imkoniyati qo'shildi (ixtiyoriy bo'lishi uchun blank=True qilindi)
    image = models.ImageField(upload_to='foods/', null=True, blank=True)
    
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"