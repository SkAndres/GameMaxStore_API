from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username,
                          email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255,
                                unique=True,
                                db_index=True)
    email = models.EmailField(max_length=255,
                              unique=True,
                              db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh),
                'access': str(refresh.access_token)}


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


def get_img_upload_path(instance, filename):
    return f'product-img/{instance.category.name}/{filename}'


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        null=False,
        on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=get_img_upload_path,
        null=True,
        blank=False)
    title = models.CharField(max_length=190,
                             blank=False)
    color = models.CharField(max_length=30,
                             blank=True)
    memory = models.IntegerField(blank=True)
    price = models.FloatField(blank=True)
    description = models.TextField(blank=False)
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(0)],
        blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class OrderAddress(models.Model):
    first_name = models.CharField(max_length=50,
                                  blank=True)
    last_name = models.CharField(max_length=50,
                                 blank=True)
    email = models.EmailField(max_length=125,
                              blank=True)
    phone_number = PhoneNumberField(blank=True)
    address = models.CharField(max_length=300,
                               blank=True)
    exact_address = models.CharField(max_length=70,
                                     null=True,
                                     blank=True)
    city = models.CharField(max_length=50,
                            null=True,
                            blank=True)
    state = models.CharField(max_length=100,
                             null=True,
                             blank=True)
    post_code = models.CharField(max_length=6,
                                 null=True,
                                 blank=True)
    country = models.CharField(max_length=300,
                               null=True,
                               blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(User, null=True,
                             blank=True,
                             on_delete=models.CASCADE)
    order = models.ForeignKey(OrderAddress,
                              null=True,
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                null=True,
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                null=True)
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
