from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import CustomUser, NEW, CODE_VERIFIED, DONE, UserLocation
from accounts.utility import send_email, check_user_type


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    auth_status = serializers.CharField(read_only=True, required=False)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password',
                  'confirm_password', 'auth_status')

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise ValidationError("Passwords do not match.")

        email = data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)
        if user.auth_status == NEW:
            code = user.create_verify_code()
            send_email(user.email, code)
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(instance.token())
        return data


class LoginSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields['user_input'] = serializers.CharField(required=True)
        self.fields['username'] = serializers.CharField(required=False, read_only=True)

    def auth_validate(self, data):
        user_input = data.get('user_input')
        if check_user_type(user_input) == 'username':
            username = user_input
        elif check_user_type(user_input) == "email":
            user = self.get_user(email__iexact=user_input)
            username = user.username
        else:
            data = {
                'success': False,
                'message': "Siz email yoki username jo'natishingiz kerak"
            }
            raise ValidationError(data)

        authentication_kwargs = {
            self.username_field: username,
            'password': data['password']
        }

        current_user = CustomUser.objects.filter(username__iexact=username).first()

        if current_user is not None and current_user.auth_status in [NEW, CODE_VERIFIED]:
            raise ValidationError(
                {
                    'success': False,
                    'message': "Siz ro'yhatdan to'liq o'tmagansiz!"
                }
            )
        user = authenticate(**authentication_kwargs)
        if user is not None:
            self.user = user
        else:
            raise ValidationError(
                {
                    'success': False,
                    'message': "Sorry, login or password you entered is incorrect. Please check and try again!"
                }
            )

    def validate(self, data):
        self.auth_validate(data)
        if self.user.auth_status not in [DONE]:
            raise PermissionDenied("Siz login qila olmaysiz. Ruxsatingiz yo'q.")
        data = self.user.token()
        data['auth_status'] = self.user.auth_status
        data['full_name'] = self.user.full_name
        return data

    @staticmethod
    def get_user(**kwargs):
        users = CustomUser.objects.filter(**kwargs)
        if not users.exists():
            raise ValidationError(
                {
                    "success": False,
                    "message": "No active account found"
                }
            )
        return users.first()


class LoginRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        access_token_instance = AccessToken(data['access'])
        user_id = access_token_instance['user_id']
        user = get_object_or_404(CustomUser, id=user_id)
        update_last_login(None, user)
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get('email', None)
        if email is None:
            raise ValidationError(
                {
                    "success": False,
                    "message": "Email kiritishingiz shart!"
                }
            )
        user = CustomUser.objects.filter(email=email)
        if not user.exists():
            raise NotFound(detail="User not found")
        attrs['user'] = user.first()
        return attrs


class ResetPasswordSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    password = serializers.CharField(
        min_length=8, required=True, write_only=True)
    confirm_password = serializers.CharField(
        min_length=8, required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'password',
            'confirm_password',
        )

    def validate(self, attrs):
        password = attrs.get('password', None)
        confirm_password = attrs.get('confirm_password', None)

        if password != confirm_password:
            raise ValidationError(
                {
                    "success": False,
                    "message": "Parolingiz va tasdiqlash parolingiz bir biriga teng emas"
                }
            )
        if password:
            validate_password(password)
        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        instance.set_password(password)
        return super(ResetPasswordSerializer, self).update(instance, validated_data)


class UserLocationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = ('lat', 'long')


import certifi
import ssl
import geopy.geocoders
from geopy.geocoders import Nominatim
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx


class UserLocationSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

    class Meta:
        model = UserLocation
        fields = ('id', 'address')

    def get_address(self, obj):
        geolocator = Nominatim(scheme='http', user_agent='getAddr')
        coordinates = f"{obj.lat}, {obj.long}"
        location = geolocator.reverse(coordinates)
        return location.address


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email', )
