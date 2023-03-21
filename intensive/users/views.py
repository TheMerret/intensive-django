import datetime

from django.conf import settings
import django.contrib.auth
from django.contrib.auth.decorators import login_required
import django.contrib.sites.shortcuts
import django.core.mail
from django.http import HttpResponseNotFound
import django.shortcuts
import django.urls
import django.utils.timezone

import users.forms
import users.models


def signup(request):
    template = "users/signup.html"
    form = users.forms.SignupForm(request.POST or None)
    context = {"form": form}
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = settings.IS_USER_ACTIVE
        activation_url = request.build_absolute_uri(
            django.urls.reverse(
                "users:activate", kwargs=dict(username=user.username)
            )
        )
        email = form.cleaned_data["email"]
        django.core.mail.send_mail(
            "Активация аккаунта.",
            f"Перейдите по ссылке,"
            f"чтобы активировать учетную запись:\n\n{activation_url}",
            django.conf.settings.FEEDBACK_EMAIL,
            [email],
            fail_silently=False,
        )
        user.save()
        profile = users.models.Profile(user=user)
        profile.save()
        return django.shortcuts.render(request, "users/signup_done.html")
    return django.shortcuts.render(request, template, context=context)


def activate(request, username):
    template = "users/activate_done.html"
    user = django.shortcuts.get_object_or_404(
        users.models.User, username=username
    )
    success = False
    status_code = 410
    timedelta_ago_joined = user.date_joined - django.utils.timezone.localtime()
    timedelta_ago_joined -= datetime.timedelta(
        microseconds=timedelta_ago_joined.microseconds
    )
    if timedelta_ago_joined <= datetime.timedelta(hours=12):
        user.is_active = True
        user.save()
        success = True
        status_code = 200
    context = {"success": success}
    return django.shortcuts.render(
        request, template, context=context, status=status_code
    )


def users_list(request):
    if not request.user.is_superuser:
        raise HttpResponseNotFound()
    template = "users/users_list.html"
    users_list = users.models.UserProxy.objects.all()
    context = {"users": users_list}
    return django.shortcuts.render(request, template, context=context)


def user_detail(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseNotFound()
    template = "users/user_detail.html"
    user = django.shortcuts.get_object_or_404(users.models.User, pk=user_id)
    context = {"user": user}
    return django.shortcuts.render(request, template, context=context)


@login_required
def profile(request):
    template = "users/profile.html"
    user_form = users.forms.UserForm(
        request.POST or None, instance=request.user
    )
    profile_form = users.forms.ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user.profile,
    )
    context = {"forms": (user_form, profile_form)}
    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        return django.shortcuts.redirect("users:profile")
    return django.shortcuts.render(request, template, context)
