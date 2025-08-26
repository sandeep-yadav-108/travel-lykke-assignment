from django.contrib import admin
from .models import TravelOption, Booking

@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ['travel_id', 'type', 'source', 'destination', 'date_time', 'price', 'available_seats']
    list_filter = ['type', 'source', 'destination', 'date_time']
    search_fields = ['source', 'destination']
    ordering = ['date_time']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'travel_option', 'number_of_seats', 'total_price', 'booking_date', 'status']
    list_filter = ['status', 'booking_date']
    search_fields = ['user__username', 'travel_option__source', 'travel_option__destination']
    readonly_fields = ['booking_date']
    ordering = ['-booking_date']
