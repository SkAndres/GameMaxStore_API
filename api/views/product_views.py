"""from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers.product_serializers import CategoriesSerializer, ProductSerializer
from api.models import Category, Product
from rest_framework import filters, generics
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


@api_view(['GET'])
def api_product_overview(request):
    api_urls = {
        'Products List': 'product-list/',
        'Product Search': 'product-list/?search=',
        'Get some product': 'get-product/<str:pk>/',

        'Categories': 'category/',
        'All prod by category': 'category/<str:pk>/',
    }
    return Response(api_urls)


class CategoryList(generics.ListAPIView):
    def get_queryset(self):
        queryset = Category.objects.all().only('id', 'name')
        return queryset
    serializer_class = CategoriesSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related(
        "category").only("id", "category", "category_id",
                         "image", "title", "color",
                         "memory", "price", "description",
                         "quantity")
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['category__name', 'title', 'price', 'color', 'memory']
    search_fields = ['category__name', 'title', 'price', 'color', 'memory']
"""