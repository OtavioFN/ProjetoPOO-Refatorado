from abc import ABC, abstractmethod
import time

class DeliveryStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, total):
        pass

    @abstractmethod
    def get_estimated_time(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

class StandardDelivery(DeliveryStrategy):
    def calculate_cost(self, total):
        if total >= 500.00:
            return 0.00
        return 25.00

    def get_estimated_time(self):
        return "7-10 days"

    def get_name(self):
        return "Standard"

class ExpressDelivery(DeliveryStrategy):
    def calculate_cost(self, total):
        return 75.00

    def get_estimated_time(self):
        return "2-3 days"
    
    def get_name(self):
        return "Express"

class DeliveryFactory:
    def create_delivery_strategy(self, method):
        method = method.lower()
        if method == 'standard':
            return StandardDelivery()
        elif method == 'express':
            return ExpressDelivery()
        elif method == 'courier':
            from Classes.CourierAdapter import CourierAdapter, ExternalCourierAPI
            return CourierAdapter(ExternalCourierAPI())
        else:
            raise ValueError("Método de entrega não suportado.")