from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from products.models import ProductModel
from .forms import ContactForm
from django.core.mail import send_mail
from pages.models import ProductsModels


class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        content = super().get_context_data(**kwargs)
        content['Best_Seller'] = ProductsModels.objects.all()
        content['Tops'] = ProductsModels.objects.all()

        return content


class ContactTemplateView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('pages:thank_you')
    login_url = 'users:login'

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        send_mail(
            'Sizga taklifim bor !',
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            'ahmedovafazilat300@gmail.com.com',
            ['ahmedovafazilat300@gmail.com'],
            fail_silently=False,
        )
        return super().form_valid(form)


class ThankYouView(TemplateView):
    template_name = 'thank_you.html'
    login_url = 'users:login'


