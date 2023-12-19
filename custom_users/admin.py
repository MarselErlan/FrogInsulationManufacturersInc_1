from django.contrib import admin
from .models import Client, DeliveryAddress

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'customer_name', 'customer_email', 'customer_phone', 'age', 'gender', 'registration_date')
    search_fields = ('username', 'customer_name', 'customer_email')
    list_filter = ('gender', 'registration_date')
    ordering = ('-registration_date',)

@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('client', 'address_line1', 'city', 'state', 'postal_code',  'created_at', 'updated_at')
    search_fields = ('client__username', 'client__customer_name', 'address_line1', 'city', 'postal_code')
    list_filter = ('city', 'state', 'created_at')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('client')
        return queryset
