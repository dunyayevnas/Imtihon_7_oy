from django.contrib import admin
from pages.models import ProductsModels, CategoryModels
# Register your models here.
admin.site.register(CategoryModels)
admin.site.register(ProductsModels)

