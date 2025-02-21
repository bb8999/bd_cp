from repositories.rental import RentalRepository


class RentalService:
    def __init__(self):
        self.repo = RentalRepository()

    def get_rental_by_id(self, rental_id: int):
        return self.repo.get_rental_by_id(rental_id)

    def add_rental(self, user_id: int, car_id: int, start_date: str, end_date: str, status: str = "active") -> int:
        rental_id = self.repo.add_rental(user_id, car_id, start_date, end_date, status)
        return rental_id
    
    def get_rentals_by_user(self, user_id: int):
        return self.repo.get_rentals_by_user(user_id)

    def update_rental(self, rental_id: int, start_date: str = None, end_date: str = None, status: str = None):
        return self.repo.update_rental(rental_id, start_date, end_date, status)

    def delete_rental(self, rental_id: int):
        self.repo.delete_rental(rental_id)

    def get_cities(self):
        return self.repo.get_cities()

    def get_fleets(self):
        return self.repo.get_fleets()

    def get_cars(self):
        return self.repo.get_cars()

    def get_available_cars(self):
        return self.repo.get_available_cars()

    def get_car_info(self, car_id: int):
        return self.repo.get_car_info(car_id)
    
    def add_car(self, name: str, fuel_type: str, transmission_type: str, rental_cost_per_day: float, fleet_id: int):
        return self.repo.add_car(name, fuel_type, transmission_type, rental_cost_per_day, fleet_id)

    def delete_car(self, car_id: int):
        return self.repo.delete_car(car_id)

    def get_fleets(self):
        return self.repo.get_fleets()

    def delete_fleet(self, fleet_id: int):
        return self.repo.delete_fleet(fleet_id)

    def get_users(self):
        return self.repo.get_users()

    def delete_user(self, user_id: int):
        return self.repo.delete_user(user_id)
    
    def delete_rental(self, rental_id: int):
        return self.repo.delete_rental(rental_id)
