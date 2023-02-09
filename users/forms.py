from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='Введите email',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'})
    )
    username = forms.CharField(
        label='Введите логин',
        required=True,
        help_text='Нельзя вводить символы: @, /, _',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'})
    )
    password1 = forms.CharField(
        label='Введите пароль',
        required=True,
        help_text='Пароль не должен быть маленьким и простым',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'})
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
        email = forms.EmailField(
            label='Введите email',
            required=True,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'})
        )
        username = forms.CharField(
            label='Введите логин',
            required=True,
            help_text='Нельзя вводить символы: @, /, _',
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'})
        )

        class Meta:
            model = User
            fields = ['email', 'username']


class ProfileImagesForm(forms.ModelForm):
    img = forms.ImageField(
        label='Загрузить фото',
        required=False,
        widget=forms.FileInput #Что бы убрать кнопку "Очистить"
    )

    class Meta:
        model = Profile
        fields = ['img']
