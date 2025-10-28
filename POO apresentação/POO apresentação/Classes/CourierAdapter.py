class ExternalCourierAPI:
    def estimate_fee(self, weight, distance_km):
        return 5.0 + 0.5 * distance_km + 0.2 * weight
    def transit_time(self, distance_km):
        return f"{1 + distance_km//10} days"
class CourierAdapter:
    def __init__(self, api):
        self._api = api
    def calculate_cost(self, total):
        weight = max(1, total/50)
        distance = 10
        return self._api.estimate_fee(weight, distance)
    def get_estimated_time(self):
        distance = 10
        return self._api.transit_time(distance)
    def get_name(self):
        return "CourierAPI"