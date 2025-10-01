from abc import ABC, abstractmethod

class OrderObserver(ABC):
    @abstractmethod
    def update(self, order, system_context):
        pass

class InventoryObserver(OrderObserver):
    def update(self, order, system_context):
        print("\n\t[Observer] Notificando o Gerenciador de Estoque...")
        
        products_repo = system_context.products
        
        for product_id, quantity in order.items.items():
            product = system_context.find_product_by_id(product_id)
            if product:
                print(f"\t- Diminuindo {quantity}x de '{product.name}' (ID {product_id})")