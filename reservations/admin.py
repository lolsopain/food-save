# reservations/admin.py

from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'food',
        'user',
        'delivery_type',
        'payment_method',
        'status',
        'reserved_at'
    )

    list_filter = (
        'status',
        'delivery_type',
        'payment_method'
    )

    search_fields = (
        'food__name',
        'client_name',
        'client_phone'
    )