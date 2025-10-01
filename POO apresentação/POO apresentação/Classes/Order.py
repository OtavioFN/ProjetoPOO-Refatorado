import random

class Order:
    def __init__(self, id, user, items, total, delivery_address, applied_coupon=None):
        self.id = id
        self.user = user
        self.items = items
        self.total = total
        self.status = 'Payment Approved'
        self.delivery_address = delivery_address
        self.applied_coupon = applied_coupon
        self.payment_id = f'SIM_{random.randint(1000, 9999)}'