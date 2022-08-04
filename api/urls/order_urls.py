from django.urls import path
from api.views import order_views

urlpatterns = [
    path('', order_views.api_order_overview, name='api_order_overview'),
    path('add/', order_views.NewOrder.as_view(), name='new_order'),
    path('order-history/', order_views.order_list, name='order-history'),

]
