from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from api.models import Product, Order
from .serializers.order_serializers import OrderSerializer
import celery


class TaskEmailVerify(celery.Task):

    def send_email(self, url, user):
        subject = 'Email verification'

        message = f'Hi, {user.username}, use the link below to verify your email \n {url}'

        mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        return mail_sent


class TaskPassRest(celery.Task):

    def send_email(self, url, user):
        subject = 'Reset password'

        message = f'Hi, {user.username}, Use the link below to reset your password \n {url}'

        mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        return mail_sent


class TaskOrdConf(celery.Task):

    def send_email(self, order_data):
        subject = 'New Order'
        product = Order.objects.filter(order_id=order_data.id)
        price = product[0].price

        html_message = render_to_string("email_template.html", {
            'order_data': order_data,
            'product': product,
            'price': price
        })
        plain_message = strip_tags(html_message)
        mail_sent = send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [order_data.email],
                              html_message=html_message)
        return mail_sent

