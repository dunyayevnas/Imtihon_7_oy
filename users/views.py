from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView, UpdateView, ListView
import random
from conf import settings
from products.models import ProductModel
from users.models import VerificationCodeModel, TeamModel, AccountModel

from users.forms import RegisterForm, EmailVerificationForm, LoginForm, AccountModelForm


UserModel = get_user_model()


def send_email_verification(user):
    random_code = random.randint(100000, 999999)

    if VerificationCodeModel.objects.filter(code=random_code).exists():
        send_email_verification(user)
    else:
        VerificationCodeModel.objects.create(
            code=random_code,
            user=user
        )
        try:
            send_mail(
                'Verification code',
                f'Verification code for {random_code}',
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            return True
        except Exception as e:
            print(e)
            return False


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:code')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # send verification code
        send_email_verification(user)
        return super().form_valid(form)

    def form_invalid(self, form):
        storage = messages.get_messages(self.request)
        storage.used = True
        messages.error(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))


def verify_email(request):
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            user_code = VerificationCodeModel.objects.filter(code=code).first()
            if user_code:
                UserModel.objects.filter(pk=user_code.user.pk).update(is_active=True)
                messages.success(request, 'Email verified successfully.')
                return redirect(reverse_lazy('users:login'))
            else:
                messages.error(request, 'This code is invalid')
        else:
            messages.error(request, 'Form submission error')
    else:
        form = EmailVerificationForm()

    return render(request, 'users/code.html', {'form': form})


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('pages:home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            messages.error(self.request, 'Invalid password or username')

    def form_invalid(self, form):
        storage = messages.get_messages(self.request)
        storage.used = True
        messages.error(self.request, 'Form is invalid')

        return self.render_to_response(self.get_context_data(form=form))


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect(reverse_lazy('pages:home'))



class About(TemplateView):
    template_name = 'users/about-us.html'
    model = TeamModel
    context_object_name = 'teams'

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['teams'] = TeamModel.objects.all()

        return content

class AccountView(LoginRequiredMixin, UpdateView):
    template_name = 'users/accounts.html'
    form_class = AccountModelForm
    success_url = reverse_lazy('pages:home')
    context_object_name = 'account'
    login_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        account = AccountModel.objects.get(user=self.request.user)
        return account


class CartView(ListView):
    template_name = 'users/cart.html'
    context_object_name = 'products'
    model = ProductModel

    def get_queryset(self):
        cart = self.request.session.get('cart', [])
        products = ProductModel.objects.filter(pk__in=cart)
        return products

    def calculate_total_price(self):
        cart = self.request.session.get('cart', [])
        products = ProductModel.objects.filter(pk__in=cart)
        total_price = Decimal('0.00')
        for product in products:
            product_price = product.get_price()
            if product_price is not None:
                total_price += product_price
        return total_price

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_price'] = self.calculate_total_price()
        return context


class WishlistView(ListView):
    template_name = 'users/wishlist.html'
    context_object_name = 'products'
    model = ProductModel

    def get_queryset(self):
        wish = self.request.session.get('wish', [])
        products = ProductModel.objects.filter(pk__in=wish)
        return products

    def calculate_total_price(self):
        wish = self.request.session.get('wish', [])
        products = ProductModel.objects.filter(pk__in=wish)
        total_price = Decimal('0.00')
        for product in products:
            product_price = product.get_price()
            if product_price is not None:
                total_price += product_price
        return total_price

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_price'] = self.calculate_total_price()
        return context

class Faq(TemplateView):
    template_name = 'faq.html'






