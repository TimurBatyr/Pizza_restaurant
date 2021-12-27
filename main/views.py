from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.views import View
from .models import Category, Product


def product_all(request):
    products = Product.products.all()
    return render(request, 'main/home.html', {'products': products})


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'main/products/category.html', {'category': category, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'main/products/meal.html', {'product': product})


class SearchResultsView(View):
    def get(self, request):
        queryset = None
        search_param = request.GET.get('search')
        if search_param is not None:
            queryset = Product.objects.filter(Q(title__icontains=search_param) | Q(description__icontains=search_param))
        return render(request, 'main/products/search.html', {'products': queryset})


# class ProductFilter(django_filters.FilterSet):
#
#     name = django_filters.CharFilter(lookup_expr='icontains')
#
#     price = django_filters.NumberFilter()
#     price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
#     price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
#
#     category__name = django_filters.CharFilter(lookup_expr='icontains')
#
#     class Meta:
#         model = Product
#         fields = ['name', 'price', 'category']
