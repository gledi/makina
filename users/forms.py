from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.contrib.auth import get_user_model


User = get_user_model()


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=128, required=True)
    last_name = forms.CharField(max_length=128, required=True)
    email = forms.EmailField(max_length=255, required=True)
    username = forms.CharField(max_length=128, required=True)
    password = forms.CharField(
        max_length=128, min_length=8, required=True, widget=forms.PasswordInput
    )
    password_confirm = forms.CharField(
        max_length=128, min_length=8, widget=forms.PasswordInput
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        else:
            raise ValidationError("Username taken")

    def clean_password(self):
        password = self.cleaned_data["password"]
        password_validation.validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password is None or password_confirm != password:
            raise ValidationError("Passwords don't match")
        return cleaned_data
