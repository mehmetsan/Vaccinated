from django.urls import path

from api.views import RegisterUser, LoginUser, VaccinationAPIView

urlpatterns = [
    path("register", RegisterUser.as_view(), name="register"),
    path("login", LoginUser.as_view(), name="login"),
    path("vaccination", VaccinationAPIView.as_view(), name="vaccination"),
]
