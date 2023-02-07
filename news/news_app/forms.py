from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class SignupForm(forms.Form):
    """
    User registration form
    """
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password'
    }))
    repeat_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'repeat_password'
    }))

    def clean(self):
        """
        Validation of registration
        """
        super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')

        if User.objects.filter(username=username).exists():
            self.add_error('username', 'Пользователь с данным именем уже существует')

        if password != repeat_password:
            self.add_error('password', '')
            self.add_error('repeat_password', 'Пароли не совпадают')

        if len(password) < 8:
            self.add_error('password', '')
            self.add_error('repeat_password', 'Пароль должен быть не менее 8 символов')

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        user.save()
        user = authenticate(**self.cleaned_data)
        return user


class SigninForm(forms.Form):
    """
    User authorization form
    """
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password'
    }))

    def clean(self):
        """
        Validation of authorization
        """
        super().clean()
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            self.add_error('username', 'Пользователя с данным именем не существует')
