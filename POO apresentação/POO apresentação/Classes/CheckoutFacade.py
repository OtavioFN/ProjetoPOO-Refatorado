from Classes.PaymentFactory import PaymentFactory
from Classes.Order import OrderBuilder, OrderDirector
from Classes.DeliveryFactory import DeliveryFactory
from Classes.DiscountHandler import CouponHandler, LoyaltyHandler, ShippingDiscountHandler, FinalCostHandler
class CheckoutFacade:
    def __init__(self):
        pass
    def process(self, payment_method, address, total, coupon_info, delivery_method_name, delivery_cost, system):
        factory = PaymentFactory()
        strategy = factory.create_payment_strategy(payment_method)
        approved = strategy.process_payment(total)
        if not approved:
            return False
        builder = OrderBuilder()
        director = OrderDirector(builder)
        try:
            new_order = director.construct_full_order(
                order_id=system._generate_new_id(system.orders),
                user=system.current_user.username,
                cart_items=system.cart.items.copy(),
                total=total,
                address=address,
                delivery_method=delivery_method_name,
                delivery_cost=delivery_cost,
                coupon_info=coupon_info
            )
            new_order.attach(system.inventory_observer)
            chain = CouponHandler()
            chain.set_next(LoyaltyHandler()).set_next(ShippingDiscountHandler()).set_next(FinalCostHandler())
            chain.handle(new_order)
            system.orders.append(new_order)
            new_order.notify(system)
            return True
        except Exception:
            return False