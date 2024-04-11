from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="MaxWay API",
        default_version='v1',
        description="MaxWay - birinchi milliy fast-food API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="shakhbozbek.usmonov@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    # swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),

    # admin
    path('admin/', admin.site.urls),

    # local apps
    path('api/v1/users/', include('accounts.urls'), name="accounts"),
    path('api/v1/products/', include('products.urls'), name="products"),
    path('api/v1/orders/', include('orders.urls'), name="orders"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('rest-api-auth/',
                         include('rest_framework.urls', namespace='rest_framework'))]
