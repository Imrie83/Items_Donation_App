import string

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import request


class RegisterForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label='',
    )
    surname = forms.CharField(
        max_length=255,
        required=False,
        label=''
    )
    email = forms.CharField(
        max_length=255,
        widget=forms.EmailInput,
        required=True,
        label=''
    )
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput,
        required=True,
        label=''
    )
    password2 = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput,
        required=True,
        label=''
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Imię'
        self.fields['surname'].widget.attrs['placeholder'] = 'Nazwisko'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password'].widget.attrs['placeholder'] = 'Hasło'
        self.fields['password2'].widget.attrs['placeholder'] = 'Powtórz hasło'

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        email = cleaned_data.get("email")

        if password != password2:
            raise forms.ValidationError(
                "Hasła muszą być takie same"
            )

        if not any(char in password for char in string.punctuation):
            raise forms.ValidationError(
                'Hasło musi posiadać znak specjalny'
            )
        if not any(char.isupper() for char in password):
            raise forms.ValidationError(
                'Hasło musi posiadać conajmniej jedną wielką literę'
            )
        if not any(char.islower() for char in password):
            raise forms.ValidationError(
                'Hasło musi posiadać conajmniej jedną małą literę'
            )
        if not any(char.isnumeric() for char in password):
            raise forms.ValidationError(
                'Hasło musi posiadać conajmniej jedną cyfrę'
            )
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError(
                'adres email zajęty!'
            )

        return cleaned_data


class EditUserForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label='',
    )
    surname = forms.CharField(
        max_length=255,
        required=False,
        label=''
    )
    email = forms.CharField(
        max_length=255,
        widget=forms.EmailInput,
        required=True,
        label=''
    )
    old_password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput,
        required=True,
        label=''
    )
    new_password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput,
        required=False,
        label=''
    )
    new_password2 = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput,
        required=False,
        label=''
    )

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Imię'
        self.fields['surname'].widget.attrs['placeholder'] = 'Nazwisko'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['new_password'].widget.attrs['placeholder'] = 'Nowe hasło'
        self.fields['new_password2'].widget.attrs[
            'placeholder'] = 'Powtórz hasło'
        self.fields['old_password'].widget.attrs[
            'placeholder'] = 'Obecne hasło'

    def clean(self):
        cleaned_data = super(EditUserForm, self).clean()
        password = cleaned_data.get("new_password")
        password2 = cleaned_data.get("new_password2")
        old_password = cleaned_data.get('old_password')
        email = cleaned_data.get('email')

        if password != password2:
            raise forms.ValidationError(
                "Hasła muszą być takie same"
            )

        if not any(char in password for char in string.punctuation):
            raise forms.ValidationError(
                'Hasło musi posiadać znak specjalny'
            )
        if not any(char.isupper() for char in password):
            raise forms.ValidationError(
                'Hasło musi posiadać conajmniej jedną wielką literę'
            )
        if not any(char.islower() for char in password):
            raise forms.ValidationError(
                'Hasło musi posiadać conajmniej jedną małą literę'
            )
        if not any(char.isnumeric() for char in password):
            raise forms.ValidationError(
                'Hasło musi posiadać conajmniej jedną cyfrę'
            )
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError(
                'adres email zajęty!'
            )
        return cleaned_data
