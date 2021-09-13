from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control m-2 data','placeholder':'Enter your username',}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control m-2 data','placeholder':"Enter Your Password",})) 
    class Meta:
        model = User
        fields = {'username','password'}

    