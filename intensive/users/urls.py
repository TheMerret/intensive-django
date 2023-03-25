import django.contrib.auth.views
import django.urls

import users.forms
import users.views


app_name = "users"

urlpatterns = [
    django.urls.path(
        "login/",
        django.contrib.auth.views.LoginView.as_view(
            template_name="users/login.html",
            authentication_form=users.forms.LoginForm,
        ),
        name="login",
    ),
    django.urls.path(
        "logout/",
        django.contrib.auth.views.LogoutView.as_view(
            template_name="users/logout.html"
        ),
        name="logout",
    ),
    django.urls.path(
        "password-change",
        django.contrib.auth.views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            success_url=django.urls.reverse_lazy("users:password-change-done"),
            form_class=users.forms.PasswordChangeForm,
        ),
        name="password-change",
    ),
    django.urls.path(
        "password-change-done",
        django.contrib.auth.views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html"
        ),
        name="password-change-done",
    ),
    django.urls.path(
        "password-reset",
        django.contrib.auth.views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            email_template_name="users/password_reset_email.html",
            success_url=django.urls.reverse_lazy("users:password-reset-done"),
            form_class=users.forms.PasswordResetForm,
        ),
        name="password-reset",
    ),
    django.urls.path(
        "password-reset-done",
        django.contrib.auth.views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password-reset-done",
    ),
    django.urls.path(
        "password-reset-confirm/<uidb64>/<token>/",
        django.contrib.auth.views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=django.urls.reverse_lazy(
                "users:password-reset-complite"
            ),
            form_class=users.forms.SetPasswordForm,
        ),
        name="password-reset-confirm",
    ),
    django.urls.path(
        "password-reset-complite",
        django.contrib.auth.views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complite.html"
        ),
        name="password-reset-complite",
    ),
    django.urls.path("signup", users.views.signup, name="signup"),
    django.urls.path(
        "activate/<str:username>", users.views.activate, name="activate"
    ),
    django.urls.path("users-list", users.views.users_list, name="users-list"),
    django.urls.path(
        "user-detail/<int:user_id>",
        users.views.user_detail,
        name="user-detail",
    ),
    django.urls.path("profile", users.views.profile, name="profile"),
    django.urls.path(
        "reactivate/<str:token>", users.views.reactivate, name="reactivate"
    ),
]
