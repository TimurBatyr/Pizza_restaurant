from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
import django_filters
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import ProductForm, UpdateProductForm, CommentForm
from .models import Category, Product, Comment


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'main/index.html'
    context_object_name = 'products'
    paginate_by = 3


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


class IsAdminCheckMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser


class ProductCreateView(IsAdminCheckMixin, CreateView):
    model = Product
    template_name = 'main/create_meal.html'
    form_class = ProductForm
    success_url = reverse_lazy('main:main_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_form'] = self.get_form(self.get_form_class())
        return context


class ProductUpdateView(IsAdminCheckMixin, UpdateView):
    model = Product
    template_name = 'main/update.html'
    form_class = UpdateProductForm
    pk_url_kwarg = 'product_id'
    success_url = reverse_lazy('main:main_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_form'] = self.get_form(self.get_form_class())
        return context


class DeleteProductView(IsAdminCheckMixin, DeleteView):
    queryset = Product.objects.all()
    template_name = 'main/delete_product.html'
    success_url = reverse_lazy('main:main_home')


class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'main/add_comment.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['product_id']
        return super().form_valid(form)
    success_url = reverse_lazy('main:main_home')

