from Classes.Product import Product
class ProductDecorator(Product):
    def __init__(self, product):
        self._product = product
    @property
    def id(self):
        return self._product.id
    @property
    def name(self):
        return self._product.name
    @property
    def description(self):
        return self._product.description
    @property
    def price(self):
        return self._product.price
class SaleDecorator(ProductDecorator):
    def __init__(self, product, percent):
        super().__init__(product)
        self._percent = percent
    @property
    def price(self):
        return round(self._product.price * (1 - self._percent / 100), 2)