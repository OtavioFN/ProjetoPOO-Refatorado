from abc import abstractclassmethod

class Coupon:
    def __init__(self, code, value, active=True):
        self.code = code
        self.value = value
        self.active = active
    
    @abstractclassmethod
    def apply_discount(self, total):
        pass

    @abstractclassmethod
    def get_display_info(self):
        pass

class PercentageCoupon(Coupon):
    def apply_discount(self, total):
        return total * (self.value / 100)
    
    def get_display_info(self):
        return f"\t- {self.code} | Percentage | {self.value}% | {'Active' if self.active else 'Inactive'}"

class FixedCoupon(Coupon):
    def apply_discount(self, total):
        return self.value

    def get_display_info(self):
        return f"\t- {self.code} | Fixed | $ {self.value:.2f} | {'Active' if self.active else 'Inactive'}"
