import streamlit as st
from services.auth_service import AuthService

def registration() :
    st.title("Регистрация пользователя")
    
    name = st.text_input("Имя")
    email = st.text_input("Email")
    password = st.text_input("Пароль", type="password")
    password_confirm = st.text_input("Подтвердите пароль", type="password")

    if st.button("Зарегистрироваться"):
        if password != password_confirm:
            st.error("Пароли не совпадают!")
        else:
            try:
                auth_service = AuthService()
                auth_service.register_user(name, email, password)
                st.success("Пользователь успешно зарегистрирован!")
            except ValueError as e:
                st.error(str(e))