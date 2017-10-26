from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, UserType, HealthProfile, MessageBox, Message


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user_type','date_of_birth', 'gender', 'introduction','phone','address','photo')

class UserTypeForm(forms.ModelForm):
    class Mete:
        model = UserType
        fields = ('user_type')

class HealthProfileEditForm(forms.ModelForm):
    class Meta:
        model = HealthProfile
        fields = ('height','weight','blood_pressure','Blood_sugar')

class MessageForm(forms.ModelForm):
    class Meta:
        model = MessageBox
        fields = ('text',)

class RequestForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)