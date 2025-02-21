'''import streamlit as st
from services.rental_service import RentalService

def render_add_car_page():
    st.title("Добавление автомобиля")

    if st.session_state.user_role != "admin":
        st.error("У вас не доступа.")
        return
    
    car_service = RentalService()

    car_name = st.text_input("Название автомобиля")
    fuel_type = st.selectbox("Тип топлива", ["Бензин", "Дизель", "Электро", "Гибрид"])
    transmission_type = st.selectbox("Коробка передач", ["Механика", "Автомат"])
    rental_cost_per_day = st.number_input("Стоимость аренды в день (руб.)", min_value=0.0, step=0.01, format="%.2f")

    fleets = car_service.get_fleets()
    if not fleets:
        st.error("Нет доступных автопарков. Добавьте автопарк перед добавлением автомобиля.")
        return

    fleet_choices = {f"{fleet[1]} ({fleet[2]})": fleet[0] for fleet in fleets}
    selected_fleet = st.selectbox("Выберите автопарк", list(fleet_choices.keys()))

    if st.button("Добавить автомобиль"):
        try:
            if not car_name:
                st.error("Пожалуйста, заполните обязательное поле 'Название автомобиля'.")
                return

            car_service.add_car(
                name=car_name,
                fuel_type=fuel_type,
                transmission_type=transmission_type,
                rental_cost_per_day=rental_cost_per_day,
                fleet_id=fleet_choices[selected_fleet],
            )

            st.success("Автомобиль успешно добавлен!")
        except Exception as e:
            st.error(f"Ошибка: {e}")
'''