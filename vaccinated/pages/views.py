from django.shortcuts import render, redirect
from django.contrib.auth import logout

from api.models import AppUser


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        user = AppUser.objects.get(email=request.user.email)
        missing_vaccinations = user.get_missing_vaccinations()
        return render(request, "home.html", context={"missing_vaccinations": missing_vaccinations})
    else:
        return render(request, "sign_in.html")


def sign_in_page(request):
    return render(request, "sign_in.html")


def sign_out(request):
    logout(request)
    return redirect("sign_in")
