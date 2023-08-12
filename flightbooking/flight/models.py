from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    
class Flight_detail(models.Model):
    Origin=models.CharField(max_length=64,null=True)
    Destination=models.CharField(max_length=10,null=True)
    Origin_date=models.DateField(null=True)
    Origin_time=models.TimeField(null=True)
    Destination_date=models.DateField(null=True)
    Destination_time=models.TimeField(null=True)
    Seat_avaliability=models.IntegerField(null=True)
    Date_now=models.DateTimeField(default=datetime.now,blank=True)

class User_booking(models.Model):
    User_Name= models.CharField(max_length=60,null=True)
    Origin=models.CharField(max_length=64,null=True)
    Destination=models.CharField(max_length=10,null=True)
    Preferred_Seating=models.CharField(max_length=64,null=True)
    Departure_date=models.DateField(null=True)
    Return_date=models.DateField(null=True)
    Adult=models.IntegerField(null=True)
    Child=models.CharField(max_length=3,null=True)
    Infant=models.CharField(max_length=3,null=True)
    Date_now=models.DateTimeField(default=datetime.now,blank=True)
    Full_name=models.CharField(max_length=64,null=True)
    Email=models.CharField(max_length=50,null=True)
    Mobile_number=models.CharField(max_length=10,null=True)
    