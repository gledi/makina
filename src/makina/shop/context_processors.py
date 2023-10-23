from .cart import Cart


def cart_total_items(request):
    cart = Cart(request.session)
    return {"cart_items_count": cart.total_items}
