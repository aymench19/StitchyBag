from django.apps import AppConfig
import os

class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

    def ready(self):
        from django.contrib.auth.models import User

        username = os.getenv("DJANGO_ADMIN_USERNAME")
        password = os.getenv("DJANGO_ADMIN_PASSWORD")

        if username and not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                password=password
            )