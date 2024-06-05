from django.contrib import admin
from api.models import Address, AppUser, UserVaccination, Vaccination, YearlyVaccination

# Register your models here.
admin.site.register(Address)
admin.site.register(AppUser)
admin.site.register(UserVaccination)
admin.site.register(Vaccination)
admin.site.register(YearlyVaccination)
