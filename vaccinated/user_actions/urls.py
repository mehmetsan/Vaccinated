from django.urls import path

from user_actions.views import RegisterUser, LoginUser

urlpatterns = [
    path("register", RegisterUser.as_view(), name="user_actions_register"),
    path("login", LoginUser.as_view(), name="user_actions_login"),
]
