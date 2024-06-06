from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.mail import send_mail
from environment_vars import from_email

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
                "name": str(vaccination),
                "dose": vaccination.dose,
                "start": vaccination.start,
                "end": vaccination.end,
                "optional": "true" if vaccination.optional else "false"
            })
        return result

    def get_user_vaccination_summary(self):
        user_vaccinations = UserVaccination.objects.filter(user=self)

        vaccinations = Vaccination.objects.all().order_by('start')
        completed_vaccinations = Vaccination.objects.filter(id__in=user_vaccinations.values_list('vaccination', flat=True))

        current_year = datetime.now().date().year
        yearly_vaccines = YearlyVaccination.objects.all()
        completed_yearly = UserVaccination.objects.filter(user=self, date__year=current_year)
        completed_yearly_vaccines = Vaccination.objects.filter(id__in=completed_yearly)

        summary = {
            'Completed': [],
            'Upcoming': [],
            'Needed': [],
            'Missed': [],
        }

        yearly_summary = {
            'Yearly': [],
        }

        for vaccination in vaccinations:
            if vaccination.id == 38:
                print("s")

            # If the vaccination is completed
            if vaccination in completed_vaccinations:
                vaccination_status = 'Completed'
            else:
                today = datetime.now().date()
                vacc_start_months = timedelta(days=30*vaccination.start)
                vacc_end_months = timedelta(days=30*vaccination.end)
                user_age_delta = (today - self.birth_date)

                # Vaccination is in the future
                if user_age_delta < vacc_start_months:
                    vaccination_status = 'Upcoming'

                else:
                    # If the vaccination is needed now
                    if vacc_end_months >= user_age_delta:
                        vaccination_status = 'Needed'

                    # Missed the vaccination altogether
                    else:
                        vaccination_status = 'Missed'

            summary[vaccination_status].append({
                'name': str(vaccination),
                'status': vaccination_status,
                'date': vaccination.get_user_vacc_date(user=self).strftime("%d/%m/%Y"),
            })

        for vaccination in yearly_vaccines:
            if vaccination in completed_yearly_vaccines:
                yearly_summary['Yearly'].append({
                    'name': str(vaccination),
                    'status': 'Completed'
                })
            else:
                yearly_summary['Yearly'].append({
                    'name': str(vaccination),
                    'status': 'Upcoming'
                })

        return summary, yearly_summary

    def notify_user_with_email(self):
        today = datetime.today().date()
        user_age_delta = today - self.birth_date

        completed_vaccinations = UserVaccination.objects.filter(user=self, vaccination__isnull=False)
        completed_vaccinations = Vaccination.objects.filter(id__in=completed_vaccinations.values_list('vaccination', flat=True))
        completed_yearly = UserVaccination.objects.filter(user=self, yearly_vaccination__isnull=False)
        completed_yearly = YearlyVaccination.objects.filter(id__in=completed_yearly.values_list('yearly_vaccination', flat=True))

        future_vaccinations = Vaccination.objects.all().exclude(id__in=completed_vaccinations)
        yearly_vaccinations = YearlyVaccination.objects.all()
        incomplete_yearlies = yearly_vaccinations.exclude(id__in=completed_yearly)

        needed_vaccinations = []

        for vaccine in future_vaccinations:
            start_threshold = timedelta(days=30*(vaccine.start-1))
            end_threshold = timedelta(days=30*vaccine.end)
            if end_threshold >= user_age_delta >= start_threshold:
                vaccine_start_date = vaccine.get_user_vacc_date(user=self)
                if vaccine_start_date > datetime.now().date():
                    needed_vaccinations.append(vaccine)

        message = "This is a reminder that you have the following vaccinations coming up:\n\n"

        if needed_vaccinations:
            message += "Vaccinations:\n"
            for vaccine in needed_vaccinations:
                message += f"Vaccination: {str(vaccine)} , Suggested Date: {vaccine.get_user_vacc_date(user=self).strftime("%d/%m/%Y")}\n"

        if incomplete_yearlies:
            message += "\nYearly Vaccinations\n"
            for vaccine in incomplete_yearlies:
                message += f"Vaccination: {str(vaccine)}"

        send_mail(subject="Your Vaccination Reminder",
                  message=message,
                  from_email=from_email,
                  recipient_list=[self.email])


class Vaccination(models.Model):
    name = models.CharField(max_length=100)
    dose = models.IntegerField(null=True)
    start = models.IntegerField(null=True)
    end = models.IntegerField(null=True)
    optional = models.BooleanField(default=False)
    total_doses = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.name} - {self.dose}/{self.total_doses}"

    def get_user_vacc_date(self, user: AppUser):
        return user.birth_date + timedelta(days=30*self.start)


class YearlyVaccination(models.Model):
    name = models.CharField(max_length=100)
    optional = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class UserVaccination(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    vaccination = models.ForeignKey(Vaccination, on_delete=models.CASCADE, null=True, blank=True)
    yearly_vaccination = models.ForeignKey(YearlyVaccination, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True)

    def __str__(self):
        return f"{self.user} / {self.vaccination}"
