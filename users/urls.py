from django.urls import path
from users.views import LoginView, RegisterView, verify_email, logout_view, About, AccountView, CartView, WishlistView, \
    Faq

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/email',verify_email, name='code'),
    path('logout/', logout_view ,name='logout'),
    path('about/', About.as_view(), name='about'),
    path('accounts/', AccountView.as_view(), name='accounts'),
    path('cart/', CartView.as_view(), name='cart'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('faq/', Faq.as_view(), name='faq'),

]