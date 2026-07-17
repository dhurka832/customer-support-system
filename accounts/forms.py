from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User 
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ["username","first_name","last_name","email","password1","password2"]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-modern', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-modern', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-modern', 'placeholder': 'Email Address'}),
        }
