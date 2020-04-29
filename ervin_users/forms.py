from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ErvinUser


class ErvinUserCreationForm(UserCreationForm):
    class Meta:
        model = ErvinUser
        fields = ("username", "email")


class ErvinUserChangeForm(UserChangeForm):
    class Meta:
        model = ErvinUser
        fields = ("username", "email")


# vim: ai ts=4 sts=4 et sw=4
