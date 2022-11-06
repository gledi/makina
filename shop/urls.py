from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_product_list, name="product-list"),
    path("config/", views.get_stripe_config, name="product-stripe-config"),
    path("checkout/", views.create_checkout_session, name="checkout-session"),
    path("success/<int:pk>/", views.payment_success, name="payment-success"),
    path("cancel/", views.payment_cancel, name="payment-cancel"),
]
