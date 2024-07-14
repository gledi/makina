from dataclasses import dataclass

from makina.shop.models import Product


@dataclass
class CartItem:
    product: Product
    quantity: int

    @property
    def total_price(self) -> str:
        return f"{self.product.price * self.quantity:,.2f}"


class Cart:
    def __init__(self, session):
        self.session = session
        self.session["cart_items"] = self.session.get("cart_items", {})

    def add(self, product_id, quantity):
        self.session["cart_items"][product_id] = (
            self.session["cart_items"].get(product_id, 0) + quantity
        )
        self.session.modified = True

    def remove(self, product_id, quantity):
        self.session["cart_items"][product_id] = max(
            self.session["cart_items"].get(product_id, 0) - quantity, 0
        )
        if self.session["cart_items"][product_id] == 0:
            del self.session["cart_items"][product_id]
        self.session.modified = True

    @property
    def total_items(self) -> int:
        return sum(self.session["cart_items"].values())

    @property
    def total_price(self) -> str:
        quantity_lookups = {
            str(product_id): quantity
            for product_id, quantity in self.session["cart_items"].items()
        }
        product_ids = [int(key) for key in quantity_lookups]
        products = Product.objects.filter(pk__in=product_ids).all()
        total = 0
        for product in products:
            total += product.price * quantity_lookups[str(product.pk)]

        return f"{total:,.2f}"

    def clear(self):
        self.session["cart_items"] = {}
        self.session.modified = True

    def __iter__(self):
        quantity_lookups = {
            str(product_id): quantity
            for product_id, quantity in self.session["cart_items"].items()
        }
        product_ids = [int(key) for key in quantity_lookups]
        products = Product.objects.filter(pk__in=product_ids).all()

        for product in products:
            yield CartItem(
                product=product,
                quantity=quantity_lookups[str(product.pk)],
            )
