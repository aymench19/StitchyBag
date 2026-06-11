from django.urls import path

from . import views

urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'product/<int:pk>/',
        views.product_detail,
        name='product_detail'
    ),

    path(
        'cart/',
        views.cart_detail,
        name='cart'
    ),

    path(
        'cart/add/<int:product_id>/',
        views.cart_add,
        name='cart_add'
    ),

    path(
        'cart/remove/<int:product_id>/',
        views.cart_remove,
        name='cart_remove'
    ),

    path(
        'cart/update/<int:product_id>/',
        views.cart_update,
        name='cart_update'
    ),

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
        'login/',
        views.custom_login,
        name='login'
    ),

  
    path(
    'dashboard/',
    views.dashboard,
    name='dashboard'
),
path('signup/', views.signup, name='signup'),
path('my-orders/', views.my_orders, name='my_orders'),
path("order/<int:order_id>/", views.order_detail, name="order_detail"),
path("order/cancel/<int:order_id>/", views.cancel_order, name="cancel_order"),

]