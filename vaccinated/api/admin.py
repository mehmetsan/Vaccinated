from django.contrib import admin
from api.models import Address, AppUser, UserVaccination, Vaccination

# Register your models here.
admin.site.register(Address)
admin.site.register(AppUser)
admin.site.register(UserVaccination)
admin.site.register(Vaccination)
