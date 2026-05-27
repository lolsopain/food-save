# foods/admin.py

from django.contrib import admin
from .models import Food


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'restaurant',
        'price',
        'food_type',
        'is_booked'
    )

    list_filter = (
        'food_type',
        'is_booked'
    )

    search_fields = (
        'name',
        'restaurant__name'
    )