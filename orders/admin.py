from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_email', 'status', 'created_at', 'address_line1', 'address_line2', 'city', 'state', 'country', 'postal_code', 'additional_info']
    search_fields = ['customer_name', 'customer_email']
    list_filter = ['status', 'created_at']
    ordering = ['-created_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price_at_time_of_purchase']
    search_fields = ['order__customer_name', 'product__name']
    list_filter = ['order__status', 'order__created_at']
    ordering = ['-order__created_at']
