from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import CheckoutForm, SignupForm
from .models import Order, Product


class HomePageTests(TestCase):
    def test_home_page_shows_pagination_when_more_than_nine_products_exist(self):
        for index in range(10):
            Product.objects.create(name=f"Produit {index}", description="Desc", price=10, stock=5)

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "page-link")
        self.assertContains(response, "2")


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


class AdminViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
        )
        self.client.force_login(self.user)

    def test_admin_product_add_page_renders(self):
        response = self.client.get(reverse("admin:shop_product_add"))
        self.assertEqual(response.status_code, 200)

    def test_admin_product_change_page_renders(self):
        product = Product.objects.create(name="Produit test", description="Desc", price=10, stock=5)
        response = self.client.get(reverse("admin:shop_product_change", args=[product.pk]))
        self.assertEqual(response.status_code, 200)

    def test_admin_order_change_page_renders(self):
        order = Order.objects.create(
            first_name="Test",
            last_name="User",
            phone="0123456789",
            address="1 rue",
            city="Paris",
            total_price=10,
            status="pending",
        )
        response = self.client.get(reverse("admin:shop_order_change", args=[order.pk]))
        self.assertEqual(response.status_code, 200)
