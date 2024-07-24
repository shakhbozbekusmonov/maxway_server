from django.urls import path
from accounts.views import SignUpAPIView, VerifyAPIView, LoginRefreshAPIView, LogOutAPIView, ForgotPasswordAPIView, \
    ResetPasswordAPIView, LoginAPIView, UserLocationCreateAPIView, UserLocationListAPIView, UserProfileAPIView

urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    path('verify/', VerifyAPIView.as_view(), name='verify'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('login/refresh/', LoginRefreshAPIView.as_view(), name='login_refresh'),
    path('logout/', LogOutAPIView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('user-location-create/', UserLocationCreateAPIView.as_view(), name='user-location-create'),
    path('user-locations/', UserLocationListAPIView.as_view(), name='user-locations'),
]
