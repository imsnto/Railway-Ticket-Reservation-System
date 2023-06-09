from django.contrib import admin
from .models import Profile, Train, Route


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