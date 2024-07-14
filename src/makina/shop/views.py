import json

import stripe
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.reverse import reverse

from .cart import Cart
from .models import Product


def get_product_list(request):
    products = Product.objects.all()
    return render(request, "shop/product_list.html", context={"products": products})


def get_cart_details(request):
    cart = Cart(request.session)
    return render(request, "shop/cart.html", context={"cart": cart})


def get_stripe_config(request) -> JsonResponse:
    if request.method == "GET":
        return JsonResponse({"publicKey": settings.STRIPE_PUBLISHABLE_KEY})
    return JsonResponse({"message": "Method not allowed"}, status=405)


@csrf_exempt
def add_product_to_cart(request: HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body)
        cart = Cart(request.session)
        cart.add(**data)
        return JsonResponse(
            {"message": "Added successfully to cart", "total_items": cart.total_items}
        )
    return JsonResponse({"message": "Method not allowed"}, status=405)


def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    product_id = int(request.GET.get("productId", "0"))
    if product_id == 0:
        return JsonResponse({"error": "Chosen product does not exist"})

    product = get_object_or_404(Product, pk=product_id)

    success_url = reverse("payment-success", kwargs={"pk": product_id}, request=request)
    cancel_url = reverse("payment-cancel", kwargs={"pk", product_id}, request=request)

    try:
        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=cancel_url,
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price": product.price_id,
                    "quantity": 1,
                }
            ],
        )
        return JsonResponse({"sessionId": checkout_session["id"]})
    except Exception as e:  # noqa: BLE001
        return JsonResponse({"error": str(e)})


def payment_success(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "shop/payment_success.html", context={"product": product})


def payment_cancel(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "shop/payment_cancel.html", context={"product": product})
