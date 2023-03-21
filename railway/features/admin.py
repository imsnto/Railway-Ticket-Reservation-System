from django.contrib import admin
from .models import Profile, Train, Route, Booking, TicketCost
from django.contrib.auth import get_user_model

User = get_user_model()

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nid', 'phone',  'post_code')
admin.site.register(Profile, ProfileAdmin)

class TrainAdmin(admin.ModelAdmin):
    list_display = ('tr_id', 'tr_name', 'tr_source', 'tr_destination', 'tr_departure', 'tr_arrival', 'tr_total_seats')
admin.site.register(Train, TrainAdmin)

class RouteAdmin(admin.ModelAdmin):
    list_display = ['train', 'serial_no', 'stops_name', 'arrival_time', 'departure_time', 'available_seats']
admin.site.register(Route, RouteAdmin)

class BookingAdmin(admin.ModelAdmin):
    list_display = ['train', 'seat_number', 'booking_date']
admin.site.register(Booking, BookingAdmin)

class TicketCostAdmin(admin.ModelAdmin):
    list_display = ['source', 'destination', 'cost']
admin.site.register(TicketCost, TicketCostAdmin)

