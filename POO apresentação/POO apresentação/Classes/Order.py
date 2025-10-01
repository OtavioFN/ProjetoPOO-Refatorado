import random

class Order:
    def __init__(self):
        self.id = None
        self.user = None
        self.items = {}
        self.total = 0.0
        self.status = 'Pending'
        self.delivery_address = None
        self.delivery_method = None
        self.delivery_cost = 0.0
        self.applied_coupon = None
        self.payment_id = None
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, system_context):
        for observer in self._observers:
            observer.update(self, system_context)

class OrderBuilder:
    def __init__(self):
        self.order = Order()

    def reset(self, order_id):
        self.order = Order()
        self.order.id = order_id
        self.order.payment_id = f'SIM_{random.randint(1000, 9999)}'
        return self

    def set_user(self, user):
        self.order.user = user
        return self

    def set_items(self, items):
        self.order.items = items
        return self

    def set_address(self, address):
        self.order.delivery_address = address
        return self

    def set_delivery(self, delivery_method_name, delivery_cost):
        self.order.delivery_method = delivery_method_name
        self.order.delivery_cost = delivery_cost
        return self

    def set_payment_details(self, total, coupon_info):
        self.order.total = total
        self.order.applied_coupon = coupon_info
        self.order.status = 'Payment Approved'
        return self

    def build(self):
        if not all([self.order.id, self.order.user, self.order.items, self.order.delivery_address]):
            raise ValueError("Pedido incompleto: Dados essenciais ausentes.")
        
        result = self.order
        return result

class OrderDirector:
    def __init__(self, builder):
        self._builder = builder

    def construct_full_order(self, order_id, user, cart_items, total, address, delivery_method, delivery_cost, coupon_info):
        return self._builder.reset(order_id) \
                            .set_user(user) \
                            .set_items(cart_items) \
                            .set_address(address) \
                            .set_delivery(delivery_method, delivery_cost) \
                            .set_payment_details(total, coupon_info) \
                            .build()