from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    no = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.country} - {self.city} - {self.street} - {self.no} "


class AppUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=False, unique=True)
    sex = models.CharField(null=False, max_length=50, choices=[('male', 'Male'), ('female', 'Female')])
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    birth_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_missing_vaccinations(self):
        completed_vaccinations = UserVaccination.objects.filter(user=self)
        missing_vaccinations = Vaccination.objects.exclude(id__in=completed_vaccinations.values_list('id', flat=True))
        result = []
        for vaccination in missing_vaccinations:
            result.append({
                "id": vaccination.id,
                "dose": vaccination.dose,
                "start": vaccination.start,
                "end": vaccination.end,
                "optional": "true" if vaccination.optional else "false"
            })
        return result


class Vaccination(models.Model):
    name = models.CharField(max_length=100)
    dose = models.IntegerField(null=True)
    start = models.IntegerField(null=True)
    end = models.IntegerField(null=True)
    optional = models.BooleanField(default=False)
    total_doses = models.IntegerField(null=True)
    yearly = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.dose}/{self.total_doses}"


class UserVaccination(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    vaccination = models.ForeignKey(Vaccination, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} / {self.vaccination}"
