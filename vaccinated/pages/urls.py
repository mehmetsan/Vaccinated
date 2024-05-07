from django.urls import path

from pages.views import home, sign_in_page, sign_out

urlpatterns = [
    path("home", home, name="home"),
    path("sign_in", sign_in_page, name="sign_in"),
    path("sign_out", sign_out, name="sign_out"),

]
