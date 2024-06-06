import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Vaccinated.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

#exec(open('jobs/notify_users.py').read())

from api.models import AppUser

all_users = AppUser.objects.all()

for user in all_users:
    try:
        user.notify_user_with_email()
    except:
        pass
