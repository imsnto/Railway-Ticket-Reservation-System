from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    nid = models.CharField(max_length=10, primary_key=True)
    post_code = models.IntegerField()
    address = models.CharField(max_length=100, null=True)

    
    class Meta:
        db_table = 'Profile'

    
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