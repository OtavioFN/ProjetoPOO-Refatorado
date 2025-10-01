from abc import ABC, abstractmethod
import time

class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, total):
        pass

class CreditCardPayment(PaymentStrategy):
    def process_payment(self, total):
        print("\n\t[+] Processando Pagamento com Cartão de Crédito...")
        time.sleep(1)
        card_number = input("\tNúmero do Cartão: ")
        security_code = input("\tCódigo de Segurança: ")
        
        if len(card_number) == 16 and len(security_code) == 3:
            print(f"\tPagamento de $ {total:.2f} aprovado (Cartão de Crédito).")
            return True
        else:
            print("\t[ERRO] Dados do cartão inválidos. Pagamento recusado.")
            return False

class BankSlipPayment(PaymentStrategy):
    def process_payment(self, total):
        print("\n\t[+] Gerando Boleto Bancário...")
        time.sleep(1)
        bank_slip_code = "99999.00000 00000.000000 00000.000000 9 00000000000000"
        print(f"\tBoleto gerado para $ {total:.2f}. Código: {bank_slip_code}")
        print("\tPagamento precisa ser confirmado manualmente (Simulado: Aprovado).")
        time.sleep(1)
        return True

class PaymentFactory:
    def create_payment_strategy(self, method):
        method = method.lower()
        if method == 'creditcard':
            return CreditCardPayment()
        elif method == 'bankslip':
            return BankSlipPayment()
        else:
            raise ValueError("Método de pagamento não suportado.")