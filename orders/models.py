from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import ProductModel

UserModel = get_user_model()


# Create your models here.
class OrderModel(models.Model):
    objects = None
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='orders')
    status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderItem(models.Model):
    objects = None
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, null=True, related_name='orders')
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=100)
    image = models.ImageField(upload_to='orders')
    image1 = models.ImageField(upload_to='orders')

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = _('Order item')
        verbose_name_plural = _('Orders items')
