from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from accounts.models import CustomUser
from accounts.serializers import SignUpSerializer


class SignUpAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]
