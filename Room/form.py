from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Orders

class UserRegister(UserCreationForm):
    name = forms.CharField(max_length=50)
    family = forms.CharField(max_length=50, help_text='Family Name')
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User

        fields = ('username', 'email', 'password1', 'password2', 'name', 'family')


class OrderRegister(forms.Form):
    class Meta:
        model = Orders

        fields = ('order_size', 'order_amount')

