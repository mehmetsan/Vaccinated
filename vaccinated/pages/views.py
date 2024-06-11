from django.shortcuts import render, redirect
from django.contrib.auth import logout
from environment_vars import google_key
from django.views.decorators.csrf import csrf_exempt

from api.models import AppUser, TwoFactorEmailModel, get_all_vaccinations
import requests


def home(request):
    if request.user.is_authenticated:

        params = request.GET
        hospital_coords = []
        if params:
            key = google_key
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


@csrf_exempt
def sign_in_page(request, *args, **kwargs):
    if request.method == 'GET':
        return render(request, 'sign_in.html', context=kwargs)

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            app_user = AppUser.objects.get(email=email)

            if app_user.user.check_password(password):
                request.session['email'] = email
                if app_user.role == "admin":
                    return redirect('home')

                # Create Auth Token
                TwoFactorEmailModel.objects.create(user=app_user)
                return redirect('two_factor')
            return redirect('login', error='Invalid password or email')
        except Exception as e:
            return redirect('login', error='Invalid password or email')


def sign_out(request):
    logout(request)
    return redirect("sign_in")


def sign_up_page(request):
    vaccinations = get_all_vaccinations()
    return render(request, "sign_up.html", context={"vaccinations": vaccinations})


@csrf_exempt
def two_factor_page(request, *args, **kwargs):
    if request.method == 'GET':
        return render(request, 'two_factor.html', context=kwargs)

    if request.method == 'POST':
        email = request.session['email']
        code = request.POST['code']

        # Take the latest authentication code generated for the user
        user = AppUser.objects.get(email=email)
        two_step = TwoFactorEmailModel.objects.filter(user=user).last()

        if two_step.code == code:
            if two_step.is_expired():
                return redirect('two_factor', error='Code expired')
            else:
                two_step.delete()
                return redirect('home')
        else:
            return redirect('two_factor', error='Invalid code')

