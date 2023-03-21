import django.contrib.auth.forms
from django.contrib.auth.models import User
import django.core.exceptions
import django.forms

import users.models


class LoginForm(django.contrib.auth.forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class PasswordChangeForm(django.contrib.auth.forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class PasswordResetForm(django.contrib.auth.forms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class SetPasswordForm(django.contrib.auth.forms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class SignupForm(django.contrib.auth.forms.UserCreationForm):
    email = django.forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email and User.objects.filter(email=email).exists():
            raise django.core.exceptions.ValidationError(
                "Пользователь с таким email уже существует"
            )
        return email

    class Meta:
        model = users.models.UserProxy
        fields = ["username", "email", "password1", "password2"]


class UserForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = users.models.UserProxy
        fields = ("email", "first_name", "last_name")


class ProfileForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = users.models.Profile
        fields = ("birthday", "image")
        widgets = {
            "birthday": django.forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
        }
