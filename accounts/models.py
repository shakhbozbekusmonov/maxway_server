from datetime import datetime, timedelta
import random
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from geopy.distance import geodesic, distance

from accounts.managers import UserManager
from common.models import BaseModel, Media

ORDINARY_USER, MANAGER, ADMIN, SUPER_ADMIN = (
    'ordinary_user', 'manager', 'admin', 'super_admin')
NEW, CODE_VERIFIED, DONE = ('new', 'code_verified', 'done')


class CustomUser(AbstractUser, BaseModel):
    USER_ROLE_CHOICES = (
        (ORDINARY_USER, ORDINARY_USER),
        (MANAGER, MANAGER),
        (ADMIN, ADMIN),
        (SUPER_ADMIN, SUPER_ADMIN)
    )

    AUTH_STATUS_CHOICES = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE),
    )

    user_roles = models.CharField(
        max_length=31, choices=USER_ROLE_CHOICES, default=ORDINARY_USER)
    auth_status = models.CharField(
        max_length=31, choices=AUTH_STATUS_CHOICES, default=NEW)
    email = models.EmailField(unique=True,
                              validators=[RegexValidator(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')])

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def create_verify_code(self):
        code = "".join([str(random.randint(0, 10000) % 10) for _ in range(5)])
        CustomUserVerification.objects.create(
            user_id=self.id,
            code=code
        )
        return code

    def check_username(self):
        if self.username:
            normalize_username = self.username.lower()
            self.username = normalize_username

    def check_email(self):
        if self.email:
            normalize_email = self.email.lower()
            self.email = normalize_email

    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }

    def save(self, *args, **kwargs):
        self.clean()
        super(CustomUser, self).save(*args, **kwargs)

    def clean(self):
        self.check_username()
        self.check_email()
        self.hashing_password()


EMAIL_EXPIRE = 2


class CustomUserVerification(models.Model):
    code = models.CharField(max_length=5)
    is_confirmed = models.BooleanField(default=False)
    expiration_time = models.DateTimeField(null=True)

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="verify_codes")

    def __str__(self):
        return str(self.user.__str__())

    def save(self, *args, **kwargs):
        self.expiration_time = datetime.now() + timedelta(minutes=EMAIL_EXPIRE)
        super(CustomUserVerification, self).save(*args, **kwargs)


# class UserProfile(models.Model):
#     address = models.CharField(max_length=255)
#     bio = models.TextField()
#
#     avatar = models.ForeignKey(Media, on_delete=models.CASCADE)
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class UserLocation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="locations")
    lat = models.CharField(max_length=255)
    long = models.CharField(max_length=255)
    price = models.FloatField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        unique_together = ('user', 'lat', 'long')

    def save(self, *args, **kwargs):
        coordinate1 = (self.lat, self.long)
        coordinate2 = (settings.CENTER_COORDINATE_LAT, settings.CENTER_COORDINATE_LONG)
        self.price = round(geodesic(coordinate1, coordinate2).km * int(settings.PRICE_FOR_PER_KM), 2)
        return super(UserLocation, self).save(*args, **kwargs)
