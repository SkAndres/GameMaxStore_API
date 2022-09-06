"""from django.urls import path
from api.views import product_views
from rest_framework import routers
from api.views.product_views import ProductViewSet, CategoryList

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')


urlpatterns = [
    path('', product_views.api_product_overview, name='api_overview'),
    path('products/category/', CategoryList.as_view(), name='category'),
]

urlpatterns += router.urls
"""