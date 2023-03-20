from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

User = get_user_model()

class Seat(models.Model):
    train = models.ForeignKey('features.Train', on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        db_table = 'seat'


class Booking(models.Model):
    train = models.ForeignKey('features.Train', on_delete=models.CASCADE, null = True)
    seat_number = models.IntegerField()
    booking_date = models.DateField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['train', 'seat_number', 'booking_date'], name='unique_booking_constraint')
        ]
        db_table = 'booking'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    nid = models.CharField(max_length=10, primary_key=True)
    post_code = models.IntegerField()
    address = models.CharField(max_length=100, null=True)

    
    class Meta:
        db_table = 'profile'

    
class Train(models.Model):
    tr_id = models.IntegerField(primary_key=True)
    tr_name = models.CharField(max_length=100)
    tr_source = models.CharField(max_length=100)
    tr_destination = models.CharField(max_length=100)
    tr_departure = models.TimeField(auto_now=False)
    tr_arrival = models.TimeField(auto_now=False)
    tr_total_seats = models.IntegerField()

    class Meta:
        db_table = 'train'

class Route(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    serial_no = models.AutoField(primary_key=True)
    stops_name = models.CharField(max_length=100)
    arrival_time = models.TimeField(auto_now=False)
    departure_time = models.TimeField(auto_now=False)
    available_seats = models.IntegerField(default=1000)

    class Meta:
        db_table = 'route'