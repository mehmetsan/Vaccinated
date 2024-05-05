from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from user_actions.serializers import AddressSerializer, RegisterUserSerializer
from user_actions.models import AppUser


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
            except Exception as e:
                print(e)
                address.delete()

                if user:
                    user.delete()

                error_message = f"User creation failed"
                return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_201_CREATED)
