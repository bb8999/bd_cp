import streamlit as st
from view.login import login
from view.register import registration
from view.profile import profile
from view.view_cars import Cars
from view.payments import render_your_rentels
from view.admin_page import admin_page


def main():
    st.title("Сервис аренды автомобиля")

    if "page" not in st.session_state:
        st.session_state.page = "Login"

    with st.sidebar:
        st.markdown("## Навигация")
        if st.button("Войти", key="login_button"):
            st.session_state.page = "Login"
        if st.button("Регистрация", key="register_button"):
            st.session_state.page = "Register"
        if st.button("Профиль", key="profile_button"):
            st.session_state.page = "Profile"
        if st.button("Автомобили", key="cars_button"):
            st.session_state.page = "Cars"
        if st.button("Ваши аренды", key="rentals_button"):
            st.session_state.page = "Your_Rentals"
        if st.button("Админ панель", key="admin_page"):
            st.session_state.page = "Admin_Page"
            
    if st.session_state.page == "Login":
        login()
    elif st.session_state.page == "Register":
        registration()
    elif st.session_state.page == "Profile":
        profile()
    elif st.session_state.page == "Cars":
        Cars()
    elif st.session_state.page == "Your_Rentals":
        render_your_rentels()
    elif st.session_state.page == "Admin_Page":
        admin_page()


if __name__ == "__main__":
    main()
