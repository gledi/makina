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
    def total_items(self):
        return sum(self.session["cart_items"].values())
