from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from .test_setup import TestUserSetUp, TestProductSetUp, TestOrderSetUp
from rest_framework import status
import pdb
from ..models import User


class TestUserViews(TestUserSetUp):

    def test_user_overview(self):
        response = self.client.get(
            self.user_overview_url
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_auth(self):
        user = self.register_user()

        response = self.client.post(
            self.token_auth_url,
            {'email': user.email,
             'password': self.user_data['password']},
            format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_refresh(self):
        user = self.register_user()

        get_data = self.client.post(
            self.token_auth_url,
            {'email': user.email,
             'password': self.user_data['password']},
            format='json')

        ref_token = get_data.data
        ref_token.get('refresh')

        response = self.client.post(
            self.ref_token_url,
            {'refresh': ref_token.get('refresh')}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_auth_error(self):
        response = self.client.post(
            self.token_auth_url,
            {},
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration(self):
        response = self.client.post(
            self.register_url,
            data={"username": self.user_data['username'],
                  "email": self.user_data['email'],
                  "password": self.user_data['password']},
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reg_error(self):
        self.client.post(
            self.register_url,
            data={"username": self.user_data['username'],
                  "email": self.user_data['email'],
                  "password": self.user_data['password']},
            format='json')

        response = self.client.post(
            self.register_url,
            data={"username": self.user_data['username'],
                  "email": self.user_data['email'],
                  "password": self.user_data['password']},
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_email(self):
        reg_user = self.register_user()

        user = User.objects.get(email=reg_user.email)
        token = RefreshToken.for_user(user).access_token

        response = self.client.get(
            self.email_verify_url,
            {'token': str(token)},
            format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_email_error(self):
        token = ''

        response = self.client.get(
            self.email_verify_url,
            {'token': str(token)},
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_password(self):
        user = self.register_user()

        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        url_token_check = reverse(
            'password-reset-confirm',
            kwargs={'uidb64': uidb64,
                    'token': token})

        req_reset_pas = self.client.get(
            url_token_check,
            {"email": self.user_data['email']},
            format='json')

        self.assertEqual(req_reset_pas.status_code, status.HTTP_200_OK)

        set_pas_com_url = reverse('password_reset_complete')

        response = self.client.patch(
            set_pas_com_url,
            {'uidb64': req_reset_pas.data.get('uidb64'),
             'token': req_reset_pas.data.get('token'),
             'password': 'NewPassword'},
            format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_prof_data(self):
        user = self.register_user()

        auth_user = self.client.force_authenticate(user=user)

        response = self.client.put(
            self.profile_upd_url,
            {'username': 'NewUserName',
             'email': 'NewEmail@gmail.com',
             'password': 'New_password'},
            format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductTestView(TestProductSetUp):

    def test_product_overview(self):
        response = self.client.get(self.product_overview_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product(self):
        self.get_product_url = reverse(
            'get-product',
            kwargs={'pk': self.product.id}
        )
        response = self.client.get(self.get_product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_list(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category(self):
        response = self.client.get(self.category_ulr)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_prod_by_category(self):
        self.prod_by_category_url = reverse(
            'prod-by-category',
            kwargs={'pk': self.category.id}
        )
        response = self.client.get(self.prod_by_category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestOrderView(TestOrderSetUp):

    def test_order_overview(self):
        response = self.client.get(self.order_overview_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_new_order(self):
        user = self.register_user()
        auth_user = self.client.force_authenticate(user=user)
        response = self.client.post(self.new_order_url,
                                    self.order_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_history(self):
        user = self.register_user()
        auth_user = self.client.force_authenticate(user=user)
        order = self.client.post(self.new_order_url,
                                 self.order_data,
                                 format='json')
        response = self.client.get(self.order_history_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

