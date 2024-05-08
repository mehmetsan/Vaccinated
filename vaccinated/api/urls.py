from django.urls import path

from api.views import RegisterUser, LoginUser, VaccinationAPIView, UserAPIView, UserMissingVaccinationsAPIView

urlpatterns = [
    path("register", RegisterUser.as_view(), name="register"),
    path("login", LoginUser.as_view(), name="login"),
    path("vaccination", VaccinationAPIView.as_view(), name="vaccination"),
    path("user", UserAPIView.as_view(), name="user"),
    path("missing_vaccinations", UserMissingVaccinationsAPIView.as_view(), name="missing_vaccinations"),

]
