class Cart:
    def __init__(self):
        self.items = {}

    def add(self, product_id, quantity):
        if quantity > 0:
            self.items[product_id] = self.items.get(product_id, 0) + quantity
            return True
        return False

    def remove(self, product_id, quantity):
        if product_id not in self.items:
            return "not_in_cart"
        current_qty = self.items[product_id]
        if 0 < quantity < current_qty:
            self.items[product_id] -= quantity
            return "partially_removed"
        elif quantity >= current_qty:
            del self.items[product_id]
            return "fully_removed"
        return "invalid_quantity"

    def get_total(self, product_repo):
        return sum(product_repo.find_product_by_id(p_id).price * quantity for p_id, quantity in self.items.items())

    def clear(self):
        self.items.clear()

    def is_empty(self):
        return not self.items
