from repositories.connector import get_connection

class RentalRepository:
    def get_rental_by_id(self, rental_id: int):
        query = """
            SELECT 
                r.rental_id, 
                r.user_id, 
                r.car_id, 
                r.start_date, 
                r.end_date, 
                r.status,
                c.name AS car_name,
                c.rental_cost_per_day,
                ((r.end_date - r.start_date) + 1) * c.rental_cost_per_day AS total_price
            FROM rentals r
            JOIN cars c ON r.car_id = c.car_id
            WHERE r.rental_id = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (rental_id,))
                row = cur.fetchone()
                if row:
                    return dict(zip([desc[0] for desc in cur.description], row))
                return None  

    def add_rental(self, user_id: int, car_id: int, start_date: str, end_date: str, status: str = 'active') -> int:
        query = """
            INSERT INTO rentals (user_id, car_id, start_date, end_date, status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING rental_id;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (user_id, car_id, start_date, end_date, status))
                rental_id = cur.fetchone()[0]
                conn.commit()

        return rental_id


    def get_rentals_by_user(self, user_id):
        query = """
            SELECT 
                rentals.rental_id, 
                rentals.start_date, 
                rentals.end_date, 
                rentals.status, 
                cars.name AS car_name, 
                cars.rental_cost_per_day, 
                fleets.name AS fleet_name, 
                fleets.address AS fleet_address, 
                fleets.city AS city,
                payments.amount AS payment_amount
            FROM rentals
            JOIN cars ON rentals.car_id = cars.car_id
            JOIN fleets ON cars.fleet_id = fleets.fleet_id
            LEFT JOIN payments ON rentals.rental_id = payments.rental_id
            WHERE rentals.user_id = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (user_id,))
                rows = cur.fetchall()
                return [
                    {
                        "rental_id": row[0],
                        "start_date": row[1],
                        "end_date": row[2],
                        "status": row[3],
                        "car_name": row[4],
                        "rental_cost_per_day": row[5],
                        "fleet_name": row[6],
                        "fleet_address": row[7],
                        "city": row[8],
                        "payment_amount": row[9] or 0,
                    }
                    for row in rows
                ]

    def update_rental(self, rental_id: int, start_date: str = None, end_date: str = None, status: str = None):
        updates = []
        params = [rental_id]

        if start_date:
            updates.append("start_date = %s")
            params.append(start_date)
        if end_date:
            updates.append("end_date = %s")
            params.append(end_date)
        if status:
            updates.append("status = %s")
            params.append(status)

        if updates:
            query = f"""
                UPDATE rentals
                SET {', '.join(updates)}
                WHERE rental_id = %s;
            """
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, tuple(params))
                    conn.commit()

    def delete_rental(self, rental_id: int):
        query = """
            DELETE FROM rentals WHERE rental_id = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (rental_id,))
                conn.commit()

    def get_cities(self):
        query = """
            SELECT DISTINCT city FROM fleets;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return [row[0] for row in cur.fetchall()]

    def get_fleets(self):
        query = """
            SELECT fleet_id, name, city FROM fleets;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()

    def get_cars(self):
        query = """
            SELECT car_id, fleet_id, name, fuel_type, transmission_type, rental_cost_per_day FROM cars;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()

    def get_available_cars(self):
        query = """
            SELECT 
                c.car_id, 
                c.name, 
                c.fuel_type, 
                c.transmission_type, 
                c.rental_cost_per_day, 
                c.fleet_id
            FROM cars c
            LEFT JOIN rentals r ON c.car_id = r.car_id AND r.status = 'active'
            WHERE r.rental_id IS NULL; -- Фильтруем машины, которые не в аренде с активным статусом
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [
                    {
                        "car_id": row[0],
                        "name": row[1],
                        "fuel_type": row[2],
                        "transmission_type": row[3],
                        "rental_cost_per_day": row[4],
                        "fleet_id": row[5],
                    }
                    for row in rows
                ]


    def get_car_info(self, car_id: int):
        query = """
            SELECT car_id, fleet_id, name, fuel_type, transmission_type, rental_cost_per_day
            FROM cars WHERE car_id = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (car_id,))
                return cur.fetchone()

    def add_car(self, name: str, fuel_type: str, transmission_type: str, rental_cost_per_day: float, fleet_id: int):
        query = """
            INSERT INTO cars (name, fuel_type, transmission_type, rental_cost_per_day, fleet_id)
            VALUES (%s, %s, %s, %s, %s);
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (name, fuel_type, transmission_type, rental_cost_per_day, fleet_id))
                conn.commit()

    def delete_car(self, car_id: int):
        query = """
            DELETE FROM cars
            WHERE car_id = %s
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, {
                     car_id
                })
                conn.commit()


    def delete_fleet(self, fleet_id: int):
        query = """
            DELETE FROM fleets WHERE fleet_id = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (fleet_id,))
                conn.commit()
    
    def delete_user(self, user_id: int):
        query = """
            DELETE FROM users WHERE user_id = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (user_id,))
                conn.commit()

    def get_rentals(self):
        query = """
            SELECT rental_id, user_id, car_id, start_date, status FROM rentals;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()

    def get_users(self):
        query = """
            SELECT user_id, name, email, password_hash, role FROM users;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()