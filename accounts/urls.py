from django.urls import path
from accounts.views import SignUpAPIView

urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup'),
]
