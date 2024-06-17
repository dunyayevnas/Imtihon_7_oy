from django.db import models


class CategoryModels(models.Model):
    objects = None
    name = models.CharField(max_length=100)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ProductsModels(models.Model):
    objects = None
    category = models.ForeignKey(CategoryModels, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=100)
    info = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    retyting = models.IntegerField()
    discount = models.IntegerField()
    brand = models.CharField(max_length=100)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_discount(self):
        return self.discount != 0

    def is_available(self):
        return self.discount != 0

    def get_price(self):
        if self.is_discount():
            return self.price - self.discount * self.price / 100

    class Meta:
        verbose_name = 'Product'
