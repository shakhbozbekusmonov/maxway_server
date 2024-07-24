from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from accounts.models import CustomUser, NEW, CODE_VERIFIED, DONE, UserLocation
from accounts.serializers import SignUpSerializer, ResetPasswordSerializer, ForgotPasswordSerializer, LogoutSerializer, \
    LoginRefreshSerializer, LoginSerializer, UserLocationCreateSerializer, UserLocationSerializer, UserProfileSerializer
from accounts.utility import send_email, check_email


class SignUpAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]


class VerifyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')

        self.check_verify(user, code)
        return Response(
            data={
                "success": True,
                "auth_status": user.auth_status,
                "access": user.token()['access'],
                "refresh": user.token()['refresh']
            }
        )

    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(
            expiration_time__gte=datetime.now(), code=code, is_confirmed=False)
        if not verifies.exists():
            data = {
                "message": "Tasdiqlash kodingiz xato yoki eskirgan."
            }
            raise ValidationError(data)
        else:
            verifies.update(is_confirmed=True)
        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.is_active = True
            user.save()
        return True

    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.check_verification(user)
        if not user.is_confirmed:
            code = user.create_verify_code()
            send_email(user.email, code)
        else:
            data = {
                "message": "Email kiritishiniz shart."
            }
            raise ValidationError(data)
        return Response(
            {
                "success": True,
                "message": "Tasdiqlash kodingiz qaytadan yuborildi."
            }
        )

    @staticmethod
    def check_verification(user):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), is_confirmed=False)
        if verifies.exists():
            data = {
                "message": "Sizni tasdiqlash kodingiz hali ham kuchda."
            }
            raise ValidationError(data)


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class LoginRefreshAPIView(TokenRefreshView):
    serializer_class = LoginRefreshSerializer


class LogOutAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = self.request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                "success": True,
                "message": "Muvaffaqiyatli logout."
            }
            return Response(data, status=205)
        except TokenError:
            return Response(status=400)


class ForgotPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_classes = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_classes(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user = serializer.validated_data.get('user')

        if check_email(email) == "email":
            code = user.create_verify_code()
            send_email(email, code)

        return Response(
            {
                "success": True,
                "message": "Tasdiqlash kodi muvaffaqiyatli yuborildi",
                "access": user.token()['access'],
                "refresh": user.token()['refresh'],
                "auth_status": user.auth_status
            },
            status=200
        )


class ResetPasswordAPIView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResetPasswordSerializer
    http_method_names = ['put', 'patch']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        response = super(ResetPasswordAPIView, self).update(request, *args, **kwargs)
        try:
            user = CustomUser.objects.get(id=response.data.get('id'))
        except ObjectDoesNotExist as e:
            raise NotFound(detail='User topilmadi')
        return Response(
            {
                "success": True,
                "message": "Parolingiz muvaffaqiyatli o'zgartirildi",
                "access": user.token()['access'],
                "refresh": user.token()['refresh']
            }
        )



class UserLocationCreateAPIView(CreateAPIView):
    queryset = UserLocation.objects.all()
    serializer_class = UserLocationCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = UserLocationCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save(user=self.request.user)
            return Response(serializer.data)
        except IntegrityError as e:
            return Response({
                "message": "This user location is already exists",
                "code": 400
            }, status=status.HTTP_400_BAD_REQUEST)


class UserLocationListAPIView(ListAPIView):
    queryset = UserLocation.objects.all()
    serializer_class = UserLocationSerializer
    pagination_class = None

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class UserProfileAPIView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user