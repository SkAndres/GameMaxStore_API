from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.encoding import smart_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import User
from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
from api.tasks import TaskPassRest


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=200, write_only=True)
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')

        if not username.isalnum():
            raise serializers.ValidationError('The username must only contain letters & numbers')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class UserSerializerWithToken(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(
        min_length=8, write_only=True)
    email = serializers.EmailField(min_length=2)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        username = attrs.get('username')
        user = User.objects.get(email=self.context['request'].user.email)

        if email != user.email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                "error": f"The email {email} already in use"
            })

        if username != user.username and User.objects.filter(username=username).exists():
            raise serializers.ValidationError({
                "error": f"The username {username} already in use"
            })

        if password != '':
            user.password = make_password(password)

        user.email = email
        user.username = username
        user.save()

        return user

    def get_token(self, token):
        token = RefreshToken.for_user(token)
        return str(token.access_token)


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(self.context['request']).domain
            relativelink = reverse('password-reset-confirm',
                                   kwargs={'uidb64': uidb64,
                                           'token': token})
            absurl = 'http://' + current_site + relativelink
            TaskPassRest().send_email(url=absurl, user=user)
            return attrs
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                "Sorry, your email doesn't exist, please "
                "check email or register a new account")


class SetNewPasswordSerlializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=8, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            uidb64 = attrs.get('uidb64')
            token = attrs.get('token')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.only('id').get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link invalid',
                                           status.HTTP_401_UNAUTHORIZED)

            user.set_password(password)
            user.save()

            return user

        except Exception:
            raise AuthenticationFailed('The reset link invalid',
                                       status.HTTP_401_UNAUTHORIZED)

