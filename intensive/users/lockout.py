import datetime

import axes.attempts
import axes.helpers
import django.conf
import django.core.mail
import django.urls
import django.utils.timezone
import jwt

import users.models


def get_lockout_response(request, credentials):
    if request.axes_failures_since_start == axes.helpers.get_failure_limit(
        request, credentials
    ):
        first_lockout_callback(request, credentials)
    prev = django.conf.settings.AXES_LOCKOUT_CALLABLE
    django.conf.settings.AXES_LOCKOUT_CALLABLE = None
    resp = axes.helpers.get_lockout_response(request, credentials)
    django.conf.settings.AXES_LOCKOUT_CALLABLE = prev
    return resp


def first_lockout_callback(request, credentials):
    username = axes.helpers.get_client_username(request, credentials)
    try:
        user = users.models.UserProxy.objects.get(username=username)
    except users.models.UserProxy.DoesNotExist:
        return
    user.is_active = False
    user.save()
    email = user.email
    expired = django.utils.timezone.localtime() + datetime.timedelta(days=7)
    token = jwt.encode(
        {"username": user.username, "exp": expired},
        django.conf.settings.SECRET_KEY,
        algorithm="HS256",
    )
    reactivate_url = django.urls.reverse(
        "users:reactivate", kwargs=dict(token=token)
    )
    send_reactivate_email(email, request, reactivate_url)


def send_reactivate_email(email, request, reactivate_url):
    reactivate_url = request.build_absolute_uri(reactivate_url)
    django.core.mail.send_mail(
        "Восстановление.",
        f"Перейдите по ссылке,"
        f"чтобы реактивировать учетную запись:\n\n{reactivate_url}",
        django.conf.settings.FEEDBACK_EMAIL,
        [email],
        fail_silently=False,
    )
