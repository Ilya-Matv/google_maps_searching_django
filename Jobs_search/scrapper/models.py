from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Business(models.Model):
    """holds business data"""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class BusinessList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='name')
    date = models.DateTimeField(default=datetime.now(), blank=True)
    count_num = models.IntegerField(default=0)
    businesses = models.ManyToManyField(Business)

    
    def __str__(self):
        return f"Business List for {self.user.username}"