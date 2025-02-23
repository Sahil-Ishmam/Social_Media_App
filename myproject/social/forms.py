from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user']
        labels = {
            'title':'Enter title of the post',
            'content':'Write post conetent',
        }
        



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
    
