from django.urls import path
from django.contrib.auth import views as auth_views

from products.views import ProductListView, ProductDetailView, add_or_remove, add_or_remov

app_name = 'products'





urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('cart/<int:pk>/', add_or_remove, name='add_or_remove'),
    path('wish/<int:pk>/', add_or_remov, name='add_or_remov')

]
