from rest_framework import serializers

from api.models import Address


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False)


class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    first_name = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    last_name = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    confirm_password = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    age = serializers.IntegerField(required=True)
    sex = serializers.CharField(required=True, allow_blank=False, allow_null=False)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
