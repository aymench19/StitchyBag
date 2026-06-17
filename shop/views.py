from decimal import Decimal
from django.core.paginator import Paginator
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Product, Order, OrderItem, Favorite, HeroImage
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, SignupForm
from .forms import CheckoutForm
from .cart import Cart
from django.contrib.auth import get_user_model
def home(request):
    products = Product.objects.all()

    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(name__icontains=query)

    sort = request.GET.get("sort", "new")
    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    else:
        products = products.order_by("-created_at")

    paginator = Paginator(products, 8)
    page_number = request.GET.get("page")
    products_page = paginator.get_page(page_number)

    favorite_product_ids = []
    if request.user.is_authenticated:
        favorite_product_ids = list(
            Favorite.objects.filter(user=request.user).values_list("product_id", flat=True)
        )

    hero_images = HeroImage.objects.order_by("-is_active", "-created_at")
    hero_image = hero_images.first()

    return render(
        request,
        "shop/home.html",
        {
            "products": products_page,
            "query": query,
            "sort": sort,
            "favorite_product_ids": favorite_product_ids,
            "hero_images": hero_images,
            "hero_image": hero_image,
        }
    )
def custom_login(request):

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, "Connexion réussie.")
            return redirect("home")

        messages.error(request, "Identifiants incorrects. Vérifiez votre e-mail et votre mot de passe.")

    else:
        form = LoginForm()

    return render(request, "registration/login.html", {
        "form": form
    })


def signup(request):

    if request.method == "POST":

        form = SignupForm(request.POST)

        if form.is_valid():

            user = form.save()

            auth_login(request, user)
            messages.success(request, "Compte créé avec succès.")

            return redirect("home")

        messages.error(request, "Veuillez corriger les erreurs ci-dessous.")

    else:
        form = SignupForm()

    return render(request, "registration/signup.html", {
        "form": form
    })
def product_detail(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()

    return render(
        request,
        "shop/product_detail.html",
        {
            "product": product,
            "is_favorite": is_favorite,
        }
    )
def cart_add(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart = Cart(request)

    cart.add(product.id)

    messages.success(
        request,
        "Produit ajouté au panier."
    )

    return redirect("cart")

def cart_detail(request):

    cart = Cart(request)

    products = cart.get_products()

    cart_items = []

    total = Decimal("0.00")

    for product in products:

        quantity = cart.cart[
            str(product.id)
        ]

        subtotal = (
            product.price * quantity
        )

        total += subtotal

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal
        })

    context = {
        "cart_items": cart_items,
        "total": total
    }

    return render(
        request,
        "shop/cart.html",
        context
    )

def cart_update(request, product_id):

    quantity = int(
        request.POST.get(
            "quantity",
            1
        )
    )

    cart = Cart(request)

    cart.update(
        product_id,
        quantity
    )

    return redirect("cart")

def cart_remove(request, product_id):

    cart = Cart(request)

    cart.remove(product_id)

    return redirect("cart")

@login_required
def checkout(request):

    cart = Cart(request)

    products = cart.get_products()

    if not products:
        return redirect("home")

    if request.method == "POST":

        form = CheckoutForm(
            request.POST
        )

        if form.is_valid():

            order = Order.objects.create(
    user=request.user if request.user.is_authenticated else None,
    first_name=form.cleaned_data["first_name"],
    last_name=form.cleaned_data["last_name"],
    phone=form.cleaned_data["phone"],
    city=form.cleaned_data["city"],
    address=form.cleaned_data["address"],
    comment=form.cleaned_data.get("comment", ""),
    total_price=cart.get_total_price()
)

            for product in products:

                quantity = cart.cart[
                    str(product.id)
                ]

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price
                )

            cart.clear()

            messages.success(request, "Commande passée avec succès.")

            return render(
                request,
                "shop/order_result.html",
                {
                    "order": order
                }
            )

        messages.error(request, "Veuillez corriger les informations du formulaire de commande.")

    else:
        form = CheckoutForm()

    return render(
        request,
        "shop/checkout.html",
        {
            "form": form
        }
    )



@staff_member_required
def dashboard(request):

    total_products = Product.objects.count()

    total_orders = Order.objects.count()

    pending_orders = Order.objects.filter(
        status='pending'
    ).count()

    delivered_orders = Order.objects.filter(
        status='delivered'
    ).count()

    revenue = (
        Order.objects.filter(
            status='delivered'
        ).aggregate(
            total=Sum('total_price')
        )['total']
        or 0
    )

    recent_orders = Order.objects.all()[:10]

    context = {
        "total_products": total_products,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "delivered_orders": delivered_orders,
        "revenue": revenue,
        "recent_orders": recent_orders,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "shop/my_orders.html",
        {"orders": orders}
    )
@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "shop/order_detail.html",
        {"order": order}
    )
@login_required
def cancel_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if order.status == "pending":
        order.status = "canceled"
        order.save()

    return redirect("my_orders")


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    favorites = Product.objects.filter(
        favorited_by__user=request.user
    ).distinct()

    if request.method == 'POST':
        from .forms import ProfileForm
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Vos informations ont été mises à jour.")
            return redirect('profile')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        from .forms import ProfileForm
        form = ProfileForm(instance=request.user)

    return render(
        request,
        "shop/profile.html",
        {
            "orders": orders,
            "favorites": favorites,
            "form": form,
        }
    )


@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    fav, created = Favorite.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        fav.delete()
        messages.success(request, "Produit retiré des favoris.")
    else:
        messages.success(request, "Produit ajouté aux favoris.")

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        next_url = '/'

    return redirect(next_url)