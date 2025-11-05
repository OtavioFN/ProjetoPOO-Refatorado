class EcommerceException(Exception):
    """Classe base para todas as exceções customizadas do e-commerce."""
    pass

class InvalidInputError(EcommerceException):
    """Erro levantado para dados de entrada inválidos (ex: quantidade <= 0)."""
    pass

class ProductNotFoundError(EcommerceException):
    """Erro levantado quando um produto não pode ser encontrado no repositório ou no carrinho."""
    pass

class InsufficientStockError(EcommerceException):
    """Erro levantado quando a quantidade desejada excede o estoque disponível."""
    def __init__(self, product_id, requested, available, message="Estoque insuficiente."):
        self.product_id = product_id
        self.requested = requested
        self.available = available
        super().__init__(f"{message} Produto ID: {product_id}. Solicitado: {requested}, Disponível: {available}.")