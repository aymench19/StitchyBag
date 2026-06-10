from decimal import Decimal
from .models import Product


class Cart:

    SESSION_KEY = "cart"

    def __init__(self, request):

        self.request = request
        self.user = request.user

        # 👉 panier selon utilisateur connecté ou session
        if self.user.is_authenticated:
            self.cart = self.request.session.get(
                f"{self.SESSION_KEY}_{self.user.id}",
                {}
            )
        else:
            self.cart = self.request.session.get(
                self.SESSION_KEY,
                {}
            )

    # -------------------------
    # SAVE CART
    # -------------------------
    def save(self):

        if self.user.is_authenticated:
            self.request.session[
                f"{self.SESSION_KEY}_{self.user.id}"
            ] = self.cart
        else:
            self.request.session[
                self.SESSION_KEY
            ] = self.cart

        self.request.session.modified = True

    # -------------------------
    # ADD PRODUCT
    # -------------------------
    def add(self, product_id, quantity=1):

        product_id = str(product_id)

        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity

        self.save()

    # -------------------------
    # UPDATE QUANTITY
    # -------------------------
    def update(self, product_id, quantity):

        product_id = str(product_id)

        if quantity > 0:
            self.cart[product_id] = quantity
        else:
            self.cart.pop(product_id, None)

        self.save()

    # -------------------------
    # REMOVE PRODUCT
    # -------------------------
    def remove(self, product_id):

        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]

        self.save()

    # -------------------------
    # CLEAR CART
    # -------------------------
    def clear(self):

        if self.user.is_authenticated:
            self.request.session.pop(
                f"{self.SESSION_KEY}_{self.user.id}",
                None
            )
        else:
            self.request.session.pop(
                self.SESSION_KEY,
                None
            )

        self.request.session.modified = True

    # -------------------------
    # GET PRODUCTS
    # -------------------------
    def get_products(self):

        ids = self.cart.keys()

        return Product.objects.filter(
            id__in=ids
        )

    # -------------------------
    # TOTAL PRICE
    # -------------------------
    def get_total_price(self):

        total = Decimal("0.00")

        for product in self.get_products():

            quantity = self.cart.get(
                str(product.id),
                0
            )

            total += product.price * quantity

        return total

    # -------------------------
    # TOTAL ITEMS
    # -------------------------
    def __len__(self):

        return sum(self.cart.values())