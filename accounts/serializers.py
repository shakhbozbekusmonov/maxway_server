from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import CustomUser, NEW
from accounts.utility import send_email


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
