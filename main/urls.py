from django.urls import path

from .views import *

app_name = 'main'

urlpatterns = [
    path('', ProductListView.as_view(), name='main_home'),
    path('meal/<slug:slug>', product_detail, name='product_detail'),
    path('search/<slug:category_slug>/', category_list, name='category_list'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('product/create/', ProductCreateView.as_view(), name='create'),
    path('product/update/<int:product_id>/', ProductUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', DeleteProductView.as_view(), name='delete'),
    path('product/<int:product_id>/comment/', AddCommentView.as_view(), name='add_comment'),
]