from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='products/'
    )

    def __str__(self):
        return f"{self.product.name} Image"


class OrderStatus(models.TextChoices):
    PENDING = "pending", "En attente"
    PREPARING = "preparing", "En préparation"
    READY = "ready", "Préparée"
    DELIVERED = "delivered", "Livrée"
    CANCELED = "canceled", "Annulée"


class Order(models.Model):
    reference = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=20)

    address = models.TextField()

    city = models.CharField(max_length=100)

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    

    def save(self, *args, **kwargs):

        if not self.reference:
            year = timezone.now().year

            count = Order.objects.filter(
                reference__startswith=f"CMD-{year}"
            ).count()

            self.reference = (
                f"CMD-{year}-{count + 1:05d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.reference
    def can_cancel(self):
        return self.status in [
            OrderStatus.PENDING
        ]

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.order.reference}"