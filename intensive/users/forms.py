from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import django.forms

import users.models


class SignupForm(UserCreationForm):
    email = django.forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserForm(django.forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class ProfileForm(django.forms.ModelForm):

    class Meta:
        model = users.models.Profile
        fields = ("birthday", "image")
