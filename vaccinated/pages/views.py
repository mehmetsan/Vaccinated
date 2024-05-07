from django.shortcuts import render, redirect
from django.contrib.auth import logout


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request, "home.html")
    else:
        return render(request, "sign_in.html")


def sign_in_page(request):
    return render(request, "sign_in.html")


def sign_out(request):
    logout(request)
    return redirect("sign_in")
