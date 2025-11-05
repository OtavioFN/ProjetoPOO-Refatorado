from Classes.EcommerceExceptions import InvalidInputError, ProductNotFoundError

class Cart:
    def __init__(self):
        self.items = {}

    def add(self, product_id, quantity, max_stock):
        if quantity <= 0:
            raise InvalidInputError("A quantidade a ser adicionada deve ser maior que zero.")
        
        current_quantity = self.items.get(product_id, 0)
        
        if current_quantity + quantity > max_stock:
            raise InsufficientStockError(
                product_id=product_id, 
                requested=current_quantity + quantity, 
                available=max_stock,
                message="Não é possível adicionar essa quantidade ao carrinho."
            )

        self.items[product_id] = current_quantity + quantity
        return True

    def remove(self, product_id, quantity):
        if product_id not in self.items:
            raise ProductNotFoundError(f"Produto ID {product_id} não está no carrinho para ser removido.")
            
        current_qty = self.items[product_id]
        
        if quantity <= 0:
            raise InvalidInputError("A quantidade a remover deve ser positiva.")
        
        if quantity >= current_qty:
            del self.items[product_id]
            return "fully_removed"

        self.items[product_id] -= quantity
        return "partially_removed"

    def get_total(self, product_repo):
        return sum(product_repo.find_product_by_id(p_id).price * quantity for p_id, quantity in self.items.items())

    def clear(self):
        self.items.clear()

    def is_empty(self):
        return not self.items