"""from api.models import OrderAddress, Order
from rest_framework import serializers
from pro.models import Product


class OrderAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderAddress
        fields = [
            'first_name', 'last_name', 'email',
            'phone_number', 'country', 'city',
            'address', 'exact_address', 'state',
            'post_code'
        ]


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'user', 'order', 'product',
            'price', 'quantity'
        ]


class OrderSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['__all__']


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'user', 'order', 'product',
            'price', 'quantity'
        ]
"""