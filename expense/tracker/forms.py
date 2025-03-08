from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class SignupForm(UserCreationForm): #this is a model form

    password2 = forms.CharField(
        label='Confirm password (again)',
        widget=forms.PasswordInput
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        label = {'email': 'Email'}