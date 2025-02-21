from repositories.user import UserRepository
from passlib.hash import bcrypt

class AuthService:
    def __init__(self) :
        self.repo = UserRepository()

    def register_user(self, name: str, email: str, password: str, role: str = "user") :
        if self.repo.get_user_by_email(email):
            raise ValueError("Пользователь с таким email уже существует")

        hashed_password = bcrypt.hash(password)

        self.repo.add_user(name, email, hashed_password, role)
        print(f"Пользователь {email} успешно зарегистрирован")

    def authenticate_user(self, email: str, password: str) :
        user = self.repo.get_user_by_email(email)
        if user and bcrypt.verify(password, user[3]):
            return user
        return None
    
    def get_user_info(self, user_id) : 
        return self.repo.get_user_info(user_id)
    
    def add_passport(self, user_id: int, first_name: str, last_name: str, mid_name: str, passport_serires: str, passport_number: str, birth_date: str, issue_date: str):
        return self.repo.add_passport(user_id, first_name, last_name, mid_name, passport_serires, passport_number, birth_date, issue_date)

    def add_driver_license(self, user_id: int, license_number: str, issue_date: str, expiration_date: str, issuing_authority: str, category: str):
        return self.repo.add_driver_license(user_id, license_number, issue_date, expiration_date, issuing_authority, category)

    def get_documents(self, user_id: int) :
        return self.repo.get_documents(user_id)
