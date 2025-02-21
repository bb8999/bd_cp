from repositories.connector import get_connection


class UserRepository:
    def get_user_by_email(self, email: str):
        query = """
            SELECT * FROM users WHERE email = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (email,))
                return cur.fetchone()

    def add_user(self, name: str, email: str, password_hash: str, role: str = "user"):
        query = """
            INSERT INTO users (name, email, password_hash, role)
            VALUES (%s, %s, %s, %s);
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (name, email, password_hash, role))
                conn.commit()

    def get_user_info(self, user_id: int):
        query = "SELECT name, email, role FROM users WHERE id = %s"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (user_id,))
                result = cur.fetchone()
                if result:
                    return {'name': result[0], 'email': result[1], 'role': result[2]}
                else:
                    raise Exception("Пользователь не найден.")

    def add_passport(self, user_id: int, first_name: str, last_name: str, mid_name: str, passport_series: str, passport_number: str, birth_date: str, issue_date: str):
        query = """
            INSERT INTO passports (user_id, first_name, last_name, mid_name, passport_series, passport_number, birth_date, issue_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (user_id, first_name, last_name, mid_name, passport_series, passport_number, birth_date, issue_date))
                conn.commit()

    def add_driver_license(self, user_id: int, license_number: str, issue_date: str, expiration_date: str, issuing_authority: str, category: str):
        query = """
            INSERT INTO driverLicenses (user_id, license_number, issue_date, expiration_date, issuing_authority, category)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (user_id, license_number, issue_date, expiration_date, issuing_authority, category))
                conn.commit()

    def get_documents(self, user_id: int):
        query = """
            SELECT 
                p.first_name, p.last_name, p.mid_name, p.passport_series, p.passport_number, p.birth_date, p.issue_date, 
                d.license_number, d.issue_date, d.expiration_date, d.issuing_authority, category
            FROM users u
            LEFT JOIN passports p ON u.user_id = p.user_id
            LEFT JOIN driverLicenses d ON u.user_id = d.user_id
            WHERE u.user_id = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (user_id,))
                result = cur.fetchone()
                if result:
                    return {
                        "passport": {
                            "first_name": result[0],
                            "last_name": result[1],
                            "mid_name": result[2],
                            "passport_series": result[3],
                            "passport_number": result[4],
                            "birth_date": result[5],
                            "issue_date": result[6]
                        },
                        "driverLicenses": {
                            "license_number": result[7],
                            "issue_date": result[8],
                            "expiration_date": result[9],
                            "issuing_authority": result[10],
                            "category": result[11]
                        }
                    }
                else:
                    raise Exception("Документы пользователя не найдены.")
