class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Customer(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.addresses = []
        self.is_prime_member = (username == 'customer') 

    def add_address(self, nickname, street, city):
        self.addresses.append({'nickname': nickname, 'street': street, 'city': city})

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)