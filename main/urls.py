from django.urls import path

from .views import *

app_name = 'main'

urlpatterns = [
    path('', product_all, name='main_home'),
    path('meal/<slug:slug>', product_detail, name='product_detail'),
    path('search/<slug:category_slug>/', category_list, name='category_list'),
    path('search/', SearchResultsView.as_view(), name='search'),
]