from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from api.serializers.order_serializers import *
from rest_framework import generics
from rest_framework import status
from api.models import Order
from api.tasks import TaskOrdConf


@api_view(['GET'])
def api_order_overview(request):
    api_urls = {
        'Make an order': 'order/add/',
        'Order History by user': 'order-history/'
    }
    return Response(api_urls)


class NewOrder(generics.GenericAPIView):
    serializer_class = OrderSerializer

    def post(self, request):

        serializer = self.serializer_class(
            data=request.data)

        if serializer.is_valid(raise_exception=True):
            data_address = serializer.data.get('order')

            order_data = OrderAddress.objects.create(
                first_name=data_address['first_name'],
                last_name=data_address['last_name'],
                email=data_address['email'],
                phone_number=data_address['phone_number'],
                country=data_address['country'],
                city=data_address['city'],
                address=data_address['address'],
                exact_address=data_address['exact_address'],
                state=data_address['state'],
                post_code=data_address['post_code']
            )

            order_items = serializer.data.get('product')

            for prod_id in order_items:
                product = Product.objects.get(id=prod_id)
                item = Order.objects.create(
                    user=request.user,
                    order=order_data,
                    product=product,
                    price=serializer.data.get('price'),
                    quantity=serializer.data.get('quantity'),
                )
                product.quantity -= item.quantity
                product.save()

                TaskOrdConf().send_email(order_data, item, product)

            return Response(
                {'message': 'Order successfully created'},
                status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderHistorySerializer(orders, many=True)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )

