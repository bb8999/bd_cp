from datetime import datetime
from repositories.connector import get_connection

class PaymentRepository:
    def create_payment(self, rental_id : int, amount : int, card_number : int, card_expiry : int, card_cvc : int) :
        query = """
            INSERT INTO payments (rental_id, payment_date, amount, status, card_number, card_expiry, card_cvc)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING payment_id;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                payment_date = datetime.now().date()
                cur.execute(query, (
                    rental_id, 
                    payment_date, 
                    amount, 
                    "Не оплачено", 
                    card_number, 
                    card_expiry, 
                    card_cvc
                ))
                payment_id = cur.fetchone()[0]
            conn.commit()
        return payment_id

    def update_payment_status(self, payment_id : int, status : str) :
        query = """
            UPDATE payments
            SET status = %s
            WHERE payment_id = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    status, 
                    payment_id
                ))
            conn.commit()
            
    def cancel_payment(self, rental_id: int) :
        query_update_rental = """
            UPDATE rentals
            SET status = 'Отменена'
            WHERE rental_id = %s
        """
        query_update_payment = """
            UPDATE payments
            SET status = 'Отменена'
            WHERE rental_id = %s
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query_update_rental, (
                    rental_id,
                ))
                cur.execute(query_update_payment, (
                    rental_id,
                ))
                
            conn.commit()