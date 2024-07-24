from django.contrib import admin
from accounts.models import CustomUser, UserLocation, CustomUserVerification

admin.site.register(CustomUser)
admin.site.register(UserLocation)
admin.site.register(CustomUserVerification)
