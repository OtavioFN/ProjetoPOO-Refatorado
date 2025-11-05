from Classes.EcommerceExceptions import InvalidInputError

class Product:
    def __init__(self, id, name, description, price):
        
        if not isinstance(price, (int, float)) or price <= 0:
            raise InvalidInputError("O preço do produto deve ser um valor numérico positivo.")
            
        if not isinstance(id, int) or id <= 0:
            raise InvalidInputError("O ID do produto deve ser um número inteiro positivo.")
            
        self.id = id
        self.name = name
        self.description = description
        self.price = price

    def __str__(self):
        return f"Produto ID {self.id}: {self.name} - ${self.price:.2f}"