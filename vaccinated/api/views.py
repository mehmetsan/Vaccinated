from django.contrib.auth import authenticate
from django.contrib.auth.models import User, auth
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import AppUser, Vaccination, UserVaccination
from api.serializers import AddressSerializer, RegisterUserSerializer, LoginUserSerializer


class UserAPIView(APIView):
    def get(self, request):
        if self.request.user.is_authenticated:
            user = AppUser.objects.get(email=self.request.user.email)
            response = {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
            return Response(data=response)


class RegisterUser(APIView):
    serializer_class = RegisterUserSerializer

    def post(self, request):
        user_data = self.request.data
        address_data = user_data.pop('address_data')

        user_serializer = self.serializer_class(data=user_data)
        address_serializer = AddressSerializer(data=address_data)

        if user_serializer.is_valid() and address_serializer.is_valid():
            address, user = None, None

            # Create Address object
            try:
                address = address_serializer.save()
            except Exception as e:
                print(e)
                error_message = f"Invalid address provided"
                return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

            # Create base User object
            try:
                data = user_serializer.validated_data
                username = f"{data['first_name']}_{data['last_name']}"
                user = User.objects.create_user(username=username, password=data['password'], email=data['email'])

                # Create the extended AppUser object
                app_user = AppUser.objects.create(user=user, email=data['email'], age=data['age'], sex=data['sex'],
                                                  first_name=data['first_name'], last_name=data['last_name'],
                                                  address=address)

                for vaccine in data['vaccinations']:
                    vaccine = Vaccination.objects.get(id=vaccine['id'])
                    user_vaccination = UserVaccination.objects.create(
                        user=app_user,
                        vaccination=vaccine
                    )
            except Exception as e:
                print(e)
                address.delete()

                if user:
                    user.delete()

                error_message = f"User creation failed"
                return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_201_CREATED)


class LoginUser(APIView):
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user:
                auth.login(request, user)
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class VaccinationAPIView(APIView):

    def get(self, request):
        vaccines = Vaccination.objects.all()
        response = []

        for vaccine in vaccines:
            response.append({
                "id": vaccine.id,
                "name": vaccine.name,
                "dose": vaccine.dose,
                "start": vaccine.start,
                "end": vaccine.end,
                "optional": vaccine.optional
            })
        return Response(data=response, status=status.HTTP_200_OK)


class UserMissingVaccinationsAPIView(APIView):
    def get(self, request):
        user_id = self.request.query_params.get('user_id')
        user = AppUser.objects.get(id=user_id)
        missing_vaccinations = user.get_missing_vaccinations()
        return Response(data={'missing_vaccinations': missing_vaccinations})
