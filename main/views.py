from django.db.models import Q
from django.shortcuts import get_object_or_404, render
import django_filters
from django.views import View
from django.views.generic import ListView

from .models import Category, Product


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'main/index.html'
    context_object_name = 'products'
    paginate_by = 3

# def product_all(request):
#     products = Product.products.all()
#     return render(request, 'main/index.html', {'products': products})


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.products.filter(category=category)
    return render(request, 'main/category.html', {'category': category, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'main/meal.html', {'product': product})


class SearchResultsView(View):
    def get(self, request):
        queryset = None
        search_param = request.GET.get('search')
        if search_param is not None:
            queryset = Product.objects.filter(Q(title__icontains=search_param) | Q(description__icontains=search_param))
        return render(request, 'main/search.html', {'products': queryset})



