from django.test import TestCase

from .forms import CheckoutForm, SignupForm


class SignupFormTests(TestCase):
    def test_signup_rejects_weak_password(self):
        form = SignupForm(
            data={
                "username": "demo",
                "email": "demo@example.com",
                "password1": "password123",
                "password2": "password123",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)


class CheckoutFormTests(TestCase):
    def test_checkout_form_contains_comment_field(self):
        form = CheckoutForm()

        self.assertIn("comment", form.fields)
        self.assertEqual(form.fields["comment"].label, "Commentaire")
