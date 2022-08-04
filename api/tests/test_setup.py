from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from api.models import Product, Category
from api.models import User


class TestUserSetUp(APITestCase):
    def setUp(self):
        self.user_overview_url = reverse('api_user_overview')

        self.token_auth_url = reverse('token_obtain_pair')
        self.ref_token_url = reverse('token_refresh')

        self.register_url = reverse('registration')
        self.email_verify_url = reverse('email-verify')

        self.req_rest_url = reverse('request-reset-password')

        self.profile_upd_url = reverse('user-profile-update')

        self.user_data = {"username": "test",
                          "email": "test@gmail.com",
                          "password": 'gmagna123'}

        return super().setUp()

    def register_user(self):
        return User.objects.create_user(**self.user_data)

    def tearDown(self):
        return super().tearDown()


class TestProductSetUp(APITestCase):
    def setUp(self):
        self.product_overview_url = reverse('api_overview')
        self.product_list_url = reverse('products_list')
        self.category_ulr = reverse('category')

        self.category = Category.objects.create(name='1')
        self.product = Product.objects.create(
            title="iPhone 12 mini (64GB) - Green",
            image="https://gamemaxapibucket.s3.amazonaws.com/media/2989122725.jpg",
            price=700.0,
            quantity=40,
            memory=64,
            category_id=self.category.id,
            description='iPhone 12 mini (64GB) - Green'
        )

        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class TestOrderSetUp(TestUserSetUp, TestProductSetUp):
    def setUp(self):
        self.order_overview_url = reverse('api_order_overview')
        self.new_order_url = reverse('new_order')
        self.order_history_url = reverse('order-history')

        self.category = Category.objects.create(name='1')
        self.product = Product.objects.create(
            title="iPhone 12 mini (64GB) - Green",
            image="https://gamemaxapibucket.s3.amazonaws.com/media/2989122725.jpg",
            price=700.0,
            quantity=40,
            memory=64,
            category_id=self.category.id,
            description='iPhone 12 mini (64GB) - Green'
        )

        self.order_data = {
            "order": {
                "first_name": "Test",
                "last_name": "Test",
                "email": "Test@gmail.com",
                "address": "Ukraine",
                "exact_address": "008",
                "city": "Ivano-Frankivsk",
                "state": "Івано-Франківська область",
                "post_code": "76010",
                "country": "Україна",
                "phone_number": "+380737777777",
            },
            "product": [self.product.id],
            "price": "1200.00",
            "quantity": 1,
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
