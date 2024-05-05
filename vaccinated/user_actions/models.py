from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    no = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.country} - {self.region} - {self.city} - {self.street}"


class AppUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=False, unique=True)
    age = models.IntegerField(null=False)
    sex = models.CharField(null=False, max_length=50, choices=[('male', 'Male'), ('female', 'Female')])
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Vaccination(models.Model):
    name = models.CharField(max_length=100)
