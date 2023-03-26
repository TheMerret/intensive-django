import datetime

import axes.models
from django.conf import settings
import django.contrib.auth
from django.contrib.auth.mixins import LoginRequiredMixin
import django.contrib.sites.shortcuts
import django.core.mail
from django.http import HttpResponseNotFound
import django.shortcuts
import django.template.loader
import django.urls
import django.utils.timezone
import django.views.generic
import jwt

import users.forms
import users.models


class SignupDoneView(django.views.generic.TemplateView):
    template_name = "users/signup_done.html"


class SignupView(django.views.generic.FormView):
    template_name = "users/signup.html"
    form_class = users.forms.SignupForm
    success_url = django.urls.reverse_lazy("users:signup-done")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = settings.IS_USER_ACTIVE
        activation_url = self.request.build_absolute_uri(
            django.urls.reverse(
                "users:activate", kwargs=dict(username=user.username)
            )
        )
        email = form.cleaned_data["email"]
        email_content = django.template.loader.render_to_string(
            "users/activate_email.html", {"activation_url": activation_url}
        )
        django.core.mail.send_mail(
            "Активация аккаунта.",
            email_content,
            django.conf.settings.FEEDBACK_EMAIL,
            [email],
            fail_silently=False,
        )
        user.save()
        profile = users.models.Profile(user=user)
        profile.save()
        return super().form_valid(form)


class ActivateView(django.views.generic.TemplateView):
    template_name = "users/activate_done.html"
    extra_context = {"success": False}

    def get(self, request, username):
        user = django.shortcuts.get_object_or_404(
            users.models.User, username=username
        )
        success = False
        status_code = 410
        timedelta_ago_joined = (
            user.date_joined - django.utils.timezone.localtime()
        )
        timedelta_ago_joined -= datetime.timedelta(
            microseconds=timedelta_ago_joined.microseconds
        )
        if timedelta_ago_joined <= datetime.timedelta(hours=12):
            user.is_active = True
            user.save()
            success = True
            status_code = 200

        self.extra_context = {"success": success}
        context = self.get_context_data()
        return self.render_to_response(context, status=status_code)


class UsersListView(django.views.generic.ListView):
    template_name = "users/users_list.html"
    model = users.models.UserProxy
    context_object_name = "users"

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise HttpResponseNotFound()
        return super().get(request, *args, **kwargs)


class UserDetailView(django.views.generic.DetailView):
    template_name = "users/user_detail.html"
    model = users.models.UserProxy
    context_object_name = "user"
    pk_url_kwarg = "user_id"

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseNotFound()
        return super().get(request, *args, **kwargs)


class ProfileDoneView(django.views.generic.TemplateView):
    template_name = "users/profile_done.html"


class ProfileView(LoginRequiredMixin, django.views.generic.UpdateView):
    template_name = "users/profile.html"
    model = users.models.UserProxy
    form_class = users.forms.UserProfileMultiForm
    success_url = django.urls.reverse_lazy("users:profile-done")

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            instance={
                "user": self.request.user,
                "profile": self.request.user.profile,
            }
        )
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        context["forms"] = (
            form["user"],
            form["profile"],
        )
        return context


def reactivate(request, token):
    template = "users/activate_done.html"
    try:
        reactivate_data = jwt.decode(
            token, settings.SECRET_KEY, algorithms="HS256"
        )
    except jwt.InvalidTokenError:
        success = False
        status_code = 401
    else:
        username = reactivate_data["username"]
        # axes.attempts.reset_user_attempts(request, credentials)
        axes.models.AccessAttempt.objects.filter(username=username).delete()
        user = django.shortcuts.get_object_or_404(
            users.models.User, username=username
        )
        user.is_active = True
        user.save()
        success = True
        status_code = 200
    context = {"success": success}
    return django.shortcuts.render(
        request, template, context=context, status=status_code
    )


class ReactivateView(django.views.generic.TemplateView):
    template_name = "users/activate_done.html"
    extra_context = {"success": False}

    def get(self, request, token):
        try:
            reactivate_data = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256"
            )
        except jwt.InvalidTokenError:
            success = False
            status_code = 401
        else:
            username = reactivate_data["username"]
            # axes.attempts.reset_user_attempts(request, credentials)
            axes.models.AccessAttempt.objects.filter(
                username=username
            ).delete()
            user = django.shortcuts.get_object_or_404(
                users.models.User, username=username
            )
            user.is_active = True
            user.save()
            success = True
            status_code = 200
        self.extra_context = {"success": success}
        context = self.get_context_data()
        return self.render_to_response(context, status=status_code)
