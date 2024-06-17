from django import template
from django.db.models import Sum

from products.models import ProductModel
from conf import settings

register = template.Library()


@register.filter
def get_user_cart(request):
    cart = request.session.get('cart', [])
    products = ProductModel.objects.filter(pk__in=cart)

    return products


@register.filter
def in_cart(product, request):
    return product.pk in request.session.get('cart', [])


@register.filter
def get_cart_total(request):
    cart = request.session.get('cart', [])
    total = ProductModel.objects.filter(pk__in=cart).aggregate(total_price=Sum('real_price'))['total_price']
    return total if total is not None else 0


@register.filter
def get_user_wishlist(request):
    wish = request.session.get('wish', [])
    products = ProductModel.objects.filter(pk__in=wish)

    return products


@register.filter
def in_wishlist(product, request):
    return product.pk in request.session.get('wish', [])


@register.filter
def get_wish_total(request):
    wish = request.session.get('wish', [])
    total = ProductModel.objects.filter(pk__in=wish).aggregate(total_price=Sum('real_price'))['total_price']
    return total if total is not None else 0


@register.simple_tag
def get_lang_url(request, lang):
    url = request.path.split('/')
    url[1] = lang
    return '/'.join(url)
