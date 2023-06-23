from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'Логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                 'placeholder': 'Пароль'}))


class AddSellForm(forms.ModelForm):
    class Meta:
        model = Sales
        exclude = ('user',)
        fields = ('fio', 'extradition', 'ti', 'kis', 'trener', 'client', 'user')
        widgets = {'fio': forms.Select(attrs={'class': 'form-control'}),
                   'extradition': forms.NumberInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Выдачи'}),
                   'ti': forms.NumberInput(attrs={'class': 'form-control',
                                                  'placeholder': 'ТИ'}),
                   'kis': forms.NumberInput(attrs={'class': 'form-control',
                                                   'placeholder': 'КИС'}),
                   'trener': forms.NumberInput(attrs={'class': 'form-control',
                                                      'placeholder': 'Тренер'}),
                   'client': forms.NumberInput(attrs={'class': 'form-control',
                                                      'placeholder': 'Клиент'}),
                   }


class AddStaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ('name', 'photo')
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control',
                                                  'placeholder': 'Введите ФИО'}),
                   'photo': forms.FileInput(attrs={'class': 'form-control'}),
                   }
        labels = {'name': '',
                  'photo': 'Выберите фото',
                  }
