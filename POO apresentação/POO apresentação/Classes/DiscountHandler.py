from abc import ABC, abstractmethod

class DiscountHandler(ABC):
    
    def __init__(self):
        self._next_handler = None
        
    def set_next(self, handler):
        self._next_handler = handler
        return handler
        
    @abstractmethod
    def handle(self, order):
        pass

    def _pass_to_next(self, order):
        if self._next_handler:
            return self._next_handler.handle(order)
        return order
        
class CouponHandler(DiscountHandler):
    def handle(self, order):
        print("\t[Chain] 1. Verificando Cupom...")
        
        if order.applied_coupon and order.applied_coupon.active:
            discount = order.applied_coupon.apply_discount(order.total)
            order.total -= discount
            print(f"\t  - CUPOM '{order.applied_coupon.code}' aplicado. Novo total: ${order.total:.2f}")
        
        return self._pass_to_next(order)

class LoyaltyHandler(DiscountHandler):
    def handle(self, order):
        print("\t[Chain] 2. Verificando Desconto de Lealdade...")
        
        if hasattr(order.user, 'is_prime_member') and order.user.is_prime_member:
            loyalty_discount = order.total * 0.10
            order.total -= loyalty_discount
            print(f"\t  - DESCONTO DE LEALDADE aplicado (-10%). Novo total: ${order.total:.2f}")
        
        return self._pass_to_next(order)

class ShippingDiscountHandler(DiscountHandler):
    def handle(self, order):
        print("\t[Chain] 3. Verificando Desconto de Frete...")
        
        SHIPPING_THRESHOLD = 400.00
        
        if order.total >= SHIPPING_THRESHOLD and order.delivery_cost > 0.00:
            original_cost = order.delivery_cost
            
            # Subtrai o custo do frete do total e zera o custo de entrega
            order.total -= original_cost
            order.delivery_cost = 0.00 
            
            print(f"\t  - DESCONTO DE FRETE GRÁTIS aplicado (Valor Original: ${original_cost:.2f}).")
        else:
            print("\t  - Regra de frete grátis não aplicada.")
            
        return self._pass_to_next(order)

class FinalCostHandler(DiscountHandler):
    def handle(self, order):
        print(f"\t[Chain] 4. Processamento Finalizado. Total do Pedido Final: ${order.total:.2f}")
        return order