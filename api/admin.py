from django.contrib import admin
from .models import Category, Product, Order, OrderAddress, User
# Register your models here.


@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ['username', 'email']


@admin.register(Category)
class Categories(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ['name']


@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ('id', 'category', 'image',
                    'title', 'price', 'description', 'quantity')
    list_filter = ('category', 'title', 'price')


@admin.register(OrderAddress)
class OrderAddress(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone_number',
                    'address', 'country', 'exact_address', 'city', 'state',
                    'post_code', 'country')
    list_filter = ('first_name', 'last_name', 'email', 'phone_number',
                   'address', 'country', 'exact_address', 'city', 'state',
                   'post_code', 'country')


@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ('id', 'user', 'order', 'product', 'quantity', 'price')
