from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms
from .models import Profile, Video

class CommentForm(forms.Form):
    text = forms.CharField(label='Comment', max_length=500)

class VideoForm(forms.Form):
    title = forms.CharField(label='Title', max_length=40)
    description = forms.CharField(label='Description', max_length=400)
    file = forms.FileField()

class ChannelForm(forms.Form):
    channel_name = forms.CharField(max_length = 50, label='Channel')
    image = forms.ImageField(required=False, help_text='Optional')

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=54, required = True)
    email = forms.EmailField(max_length=124, required=False, help_text='Optional')

    class Meta:
        model = User
        fields = ['username' , 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(label='login', max_length=54)
    password = forms.CharField(label='Password', max_length=54, widget=forms.PasswordInput)

class EditAvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

class ResetPasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta: 
        model = User
        fields = ['password']

class UpdateVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description']