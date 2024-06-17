from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from products.models import ProductModel, ProductCategoryModel, ProductBrand, ProductColor, ProductTagModel, \
    ProductSizeModel
from users.models import TeamModel


class ProductListView(ListView):
    template_name = 'products/product-list.html'
    model = ProductModel
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        qs = ProductModel.objects.all().order_by('-pk')
        cat = self.request.GET.get('cat')
        tag = self.request.GET.get('tag')
        brand = self.request.GET.get('brand')
        col = self.request.GET.get('col')
        sort = self.request.GET.get('sort')
        q = self.request.GET.get('q')
        sizes = self.request.GET.get('sizes')

        if cat:
            qs = qs.filter(categories__in=cat)
        if tag:
            qs = qs.filter(tags__in=tag)
        if brand:
            qs = qs.filter(brands__in=brand)
        if col:
            qs = qs.filter(color__in=col)
        if sizes:
            qs = qs.filter(sizes__in=sizes)
        if sort:
            if sort == '-price':
                qs = qs.order_by('-real_price')
            else:
                qs = qs.order_by('real_price')
        if sort:
            if sort == 'title':
                qs = qs.order_by('title')
            else:
                qs = qs.order_by('-title')
        if q:
            qs = qs.filter(title__icontains=q)

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        content = super().get_context_data(**kwargs)
        content['categories'] = ProductCategoryModel.objects.all()
        content['brand'] = ProductBrand.objects.all()
        content['color'] = ProductColor.objects.all()
        content['sizes'] = ProductSizeModel.objects.all()
        content['tags'] = ProductTagModel.objects.all()

        return content


class ProductDetailView(DetailView):
    template_name = 'products/product-detail.html'
    model = ProductModel
    context_object_name = 'products'

    def get_object(self, *args, **kwargs):
        return ProductModel.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        products = ProductModel.objects.get(id=self.kwargs['pk'])
        content = super().get_context_data(**kwargs)
        content.update({
            'categories': ProductCategoryModel.objects.all(),
            'brand': ProductBrand.objects.all(),
            'color': ProductColor.objects.all(),
            'tags': ProductTagModel.objects.all(),
            'product': ProductModel.objects.all(),
            'author' : TeamModel.objects.all(),
            'sizes' : ProductSizeModel.objects.all()
        })

        return content


def add_or_remove(request, pk):
    cart = request.session.get('cart', [])
    if pk in cart:
        cart.remove(pk)
    else:
        cart.append(pk)
    request.session['cart'] = cart
    return redirect(request.GET.get('next', 'products:list'))

def add_or_remov(request, pk):
    wish = request.session.get('wish', [])
    if pk in wish:
        wish.remove(pk)
    else:
        wish.append(pk)
    request.session['wish'] = wish
    return redirect(request.GET.get('next', 'products:list'))








