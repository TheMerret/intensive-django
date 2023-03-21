import datetime

import axes.attempts
import axes.helpers
import django.conf
import django.core.mail
import django.urls
import jwt

import users.models


def get_lockout_response(request, credentials):
    if request.axes_failures_since_start == axes.helpers.get_failure_limit(
        request, credentials
    ):
        send_reactivate_message(request, credentials)
    prev = django.conf.settings.AXES_LOCKOUT_CALLABLE
    django.conf.settings.AXES_LOCKOUT_CALLABLE = None
    resp = axes.helpers.get_lockout_response(request, credentials)
    django.conf.settings.AXES_LOCKOUT_CALLABLE = prev
    return resp


def send_reactivate_message(request, credentials):
    username = axes.helpers.get_client_username(request, credentials)
    try:
        user = users.models.UserProxy.objects.get(username=username)
    except users.models.UserProxy.DoesNotExist:
        return
    email = user.email
    expired = datetime.datetime.now() + datetime.timedelta(days=7)
    token = jwt.encode(
        {"username": user.username, "exp": expired},
        django.conf.settings.SECRET_KEY,
        algorithm="HS256"
    )
    reactivate_url = request.build_absolute_uri(
            django.urls.reverse(
                "users:reactivate", kwargs=dict(token=token)
            )
        )
    django.core.mail.send_mail(
        "Восстановление.",
        f"Перейдите по ссылке,"
        f"чтобы реактивировать учетную запись:\n\n{reactivate_url}",
        django.conf.settings.FEEDBACK_EMAIL,
        [email],
        fail_silently=False,
    )
