from django.urls import path

from products.views import CategoryListAPIView, ProductListAPIView, ProductDetailAPIView, CategoryRetrieveView

urlpatterns = [
    path('category-list/', CategoryListAPIView.as_view(), name='category-list'),
    path('product-list/', ProductListAPIView.as_view(), name='product-list'),
    path('product/<slug:slug>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('category/<int:pk>/', CategoryRetrieveView.as_view(), name='category-detail'),
]
