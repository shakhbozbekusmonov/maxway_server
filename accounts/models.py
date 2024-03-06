from datetime import datetime, timedelta
import random
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from common.models import BaseModel


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


EMAIL_EXPIRE = 5


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
