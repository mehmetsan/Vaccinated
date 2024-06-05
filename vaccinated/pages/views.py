from django.shortcuts import render, redirect
from django.contrib.auth import logout
from datetime import datetime, timedelta

from api.models import AppUser, UserVaccination
from api.utils import get_all_vaccinations
import requests

# Create your views here.
def home(request):
    if request.user.is_authenticated:

        params = request.GET
        hospital_coords = []
        if params:
            key = "AIzaSyBeZ2Q4BwACTPnAbJ7GHPMMp_VBF2lT6WQ"
            url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={params['lat']},{params['lng']}&radius=1000&type=hospital&key={key}"

            response = requests.get(url)

            hospitals = response.json()['results']

            for each in hospitals:
                location = each['geometry']['location']
                lat = location['lat']
                lng = location['lng']
                hospital_coords.append({
                    'lat': lat,
                    'lng': lng,
                })


        user = AppUser.objects.get(email=request.user.email)

        summary, yearly_summary = user.get_user_vaccination_summary()

        return render(request, "home.html", context={**summary, **yearly_summary, 'hospitals': hospital_coords})
    else:
        return render(request, "sign_in.html")


def sign_in_page(request):
    return render(request, "sign_in.html")


def sign_out(request):
    logout(request)
    return redirect("sign_in")


def sign_up_page(request):
    vaccinations = get_all_vaccinations()
    return render(request, "sign_up.html", context={"vaccinations": vaccinations})