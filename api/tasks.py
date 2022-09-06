"""from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from GameMax_Api.celery import app
from api.models import Order, User
from celery import shared_task


@shared_task
def send_email_verify(url, user_email, username):
    subject = 'Email verification'

    message = f'Hi, {username}, use the link below to verify your email \n {url}'

    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])

    return mail_sent


@shared_task
def send_password_reset(url, user_email, username):
    subject = 'Reset password'

    message = f'Hi, {username}, Use the link below to reset your password \n {url}'

    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])

    return mail_sent


@shared_task
def send_order_conf(order_id, order_email):
    subject = 'New Order'

    product = Order.objects.filter(order_id=order_id)

    price = product[0].price

    html_message = render_to_string("email_template.html", {
        'order_id': order_id,
        'product': product,
        'price': price
    })
    plain_message = strip_tags(html_message)
    mail_sent = send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [order_email],
                          html_message=html_message)
    return mail_sent


@app.task(bind=True)
def cleaning_of_unverified_users(*args, **kwargs):
    for user in User.objects.all():
        if not user.is_verified:
            user.delete()
    return "Done"

"""