from django.contrib import admin
from accounts.models import CustomUser, UserLocation


admin.site.register(CustomUser)
admin.site.register(UserLocation)
