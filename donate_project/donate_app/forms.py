from django import forms


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

        if password != password2:
            raise forms.ValidationError(
                "Hasła muszą być takie same"
            )
        return cleaned_data

