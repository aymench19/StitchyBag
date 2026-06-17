import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Nom d'utilisateur"
        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Nom d'utilisateur"
        })
        self.fields["password"].label = "Mot de passe"
        self.fields["password"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Mot de passe"
        })


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

        self.fields["username"].label = "Nom d'utilisateur"
        self.fields["email"].label = "Adresse e-mail"
        self.fields["password1"].label = "Mot de passe"
        self.fields["password2"].label = "Confirmer le mot de passe"

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


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "username": "Nom d'utilisateur",
            "email": "Adresse e-mail",
            "first_name": "Prénom",
            "last_name": "Nom",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


class CheckoutForm(forms.Form):

    first_name = forms.CharField(
        label="Prénom",
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )

    last_name = forms.CharField(
        label="Nom",
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )

    phone = forms.CharField(
        label="Téléphone",
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )

    city = forms.CharField(
        label="Ville",
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )

    address = forms.CharField(
        label="Adresse",
        widget=forms.Textarea(
            attrs={
                "class":"form-control",
                "rows":4
            }
        )
    )

    comment = forms.CharField(
        label="Commentaire",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class":"form-control",
                "rows":3,
                "placeholder":"Ajoutez un commentaire pour votre commande..."
            }
        )
    )

