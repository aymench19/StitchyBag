import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignupForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "form-control"
            })

    def clean_password1(self):
        password = self.cleaned_data.get("password1")

        if not password:
            return password

        if len(password) < 8:
            raise ValidationError("Le mot de passe doit contenir au moins 8 caractères.")

        if not re.search(r"[A-Z]", password):
            raise ValidationError("Le mot de passe doit contenir au moins une lettre majuscule.")

        if not re.search(r"[a-z]", password):
            raise ValidationError("Le mot de passe doit contenir au moins une lettre minuscule.")

        if not re.search(r"\d", password):
            raise ValidationError("Le mot de passe doit contenir au moins un chiffre.")

        if not re.search(r"[^A-Za-z0-9]", password):
            raise ValidationError("Le mot de passe doit contenir au moins un caractère spécial.")

        return password


class CheckoutForm(forms.Form):

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )

    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )

    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class":"form-control",
                "rows":4
            }
        )
    )

