from django.urls import path
from api.views import product_views

urlpatterns = [
    path('', product_views.api_product_overview, name='api_overview'),
    path('get-product/<str:pk>/', product_views.get_product, name='get-product'),
    path('products-list/', product_views.ProductList.as_view(), name='products_list'),
    path('category/', product_views.category, name='category'),
    path('category/<str:pk>/', product_views.prod_by_categ, name='prod-by-category'),
]
