from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'food',
        'client_name',    # Qidiruvda bor bo'lgani uchun ustun sifatida qo'shildi
        'client_phone',   # Qidiruvda bor bo'lgani uchun ustun sifatida qo'shildi
        'delivery_type',
        'payment_method',
        'status',
        # 'reserved_at' olib tashlandi, chunki modelda bunday maydon yo'q
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