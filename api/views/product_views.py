from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers.product_serializers import *
from rest_framework import filters, generics
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist


@api_view(['GET'])
def api_product_overview(request):
    api_urls = {
        'Products List': '/product-list/',
        'Product Search': '/product-list/?search=',
        'Get some product': 'get-product/<str:pk>/',

        'Categories': '/category/',
        'All prod by category': '/category/<str:pk>/',
    }
    return Response(api_urls)


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'price', 'color', 'memory']

    def get_paginated_response(self, data):
        return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def category(request):
    try:
        categ = Category.objects.all()
        serializer = CategoriesSerializer(categ, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def prod_by_categ(request, pk):
    try:
        by_categ = Product.objects.filter(category=pk)
        serializer = ProductSerializer(by_categ, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)




