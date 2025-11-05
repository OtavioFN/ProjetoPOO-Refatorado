from Classes.EcommerceExceptions import InvalidInputError

class Review:
    def __init__(self, product_id, user, rating, comment):
        # 1. Implementação da Validação com Exceção Específica
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise InvalidInputError("A avaliação (rating) deve ser um número inteiro entre 1 e 5.")
            
        self.product_id = product_id
        self.user = user
        self.rating = rating
        self.comment = comment