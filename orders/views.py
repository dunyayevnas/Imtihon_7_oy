from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.db import transaction

from orders.forms import OrderModelForm
from orders.models import OrderModel, OrderItem
from products.models import ProductModel
from users.models import AccountModel


class CheckoutView(TemplateView):
    template_name = 'products/checkout.html'


@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    new_order = OrderModel.objects.create(user=request.user, status=False)
                    cart = request.session.get('cart', None)
                    if cart is None:
                        return redirect('products:list')
                    products = ProductModel.objects.filter(pk__in=cart)
                    for product in products:
                        OrderItem.objects.create(
                            product=product,
                            product_name=product.title,
                            quantity=1,
                            size='test',
                            price=product.real_price,
                            image=product.image,
                            image1=product.image1,
                            order=new_order,
                        )
                    request.session['cart'] = []
                    return redirect('products:list')
            except Exception as e:
                print(e)
                return redirect('products:list')
        else:
            return render(request, 'products/checkout.html')


def order_history_view(request):
    if request.method == 'GET':
        orders = OrderModel.objects.filter(user=request.user)
        context = {'orders': orders}
        return render(request, 'users/order-history.html', context)

