from django.contrib import admin
from django.urls import path

from user_actions.views import RegisterUser

urlpatterns = [
    path("register", RegisterUser.as_view(), name="user_actions_register"),
]
