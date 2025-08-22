from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from myapp.models import *

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required = True)

    class Meta:
        model = Customer
        fields = ["username", "email", "password1", "password2"]

class UpdateUserForm(UserChangeForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]