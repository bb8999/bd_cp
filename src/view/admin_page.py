import streamlit as st
from services.rental_service import RentalService

def admin_page():

    if "user_id" not in st.session_state:
        st.error("Вы не авторизованы.")
        return
    
    if st.session_state.user_role != "admin":
        st.error("У вас не доступа.")
        return
    
    service = RentalService()
    st.title("Панель Админа")

    menu = st.sidebar.selectbox(
        "Select an action:",
        [
            "Добавить машину",
            "Список машин",
            "Удалить машину",
            "Список автопарков",
            "Удалить автопарк",
            "Список пользователей",
            "Удалить пользователя",
        ]
    )

    if menu == "Добавить машину":
        render_add_car_page()

    elif menu == "Список машин":
        st.header("Список машин")
        cars = service.get_cars()
        if cars:
            st.table(cars)
        else:
            st.info("Нет машин")

    elif menu == "Удалить машину":
        st.header("Удалить машину")
        car_id = st.text_input("Введите ID машины")
        if st.button("Удалить"):
            try:
                service.delete_car(car_id)
                st.success("Машина успешно удалилась!")
            except:
                st.error("Ошибка. Проверьте ID машины.")

    elif menu == "Список автопарков":
        st.header("Список автопарков")
        fleets = service.get_fleets()
        if fleets:
            st.table(fleets)
        else:
            st.info("Нет автопарков")

    elif menu == "Удалить автопарк":
        st.header("Удалить автопарк")
        fleet_id = st.text_input("Введите ID автопарка:")
        if st.button("Удалить"):
            try:
                service.delete_fleet(fleet_id)
                st.success("Автопарк успешно удалён!")
            except:
                st.error("Ошибка. Проверьте ID автопарка")

    elif menu == "Список пользователей":
        st.header("Список пользователей")
        users = service.get_users()
        if users:
            st.table(users)
        else:
            st.info("Нет пользователей.")

    elif menu == "Удалить пользователя":
        st.header("Удалить пользователя")
        user_id = st.text_input("Введите ID пользователя")
        if st.button("Удалить"):
            result = service.delete_user(user_id)
            if result:
                st.success("Пользователь успешно удалён!")
            else:
                st.error("Ошибка. Проверьте ID пользователя.")


def render_add_car_page():
    st.title("Добавление автомобиля")

    if st.session_state.user_role != "admin":
        st.error("У вас не доступа.")
        return
    
    service = RentalService()

    car_name = st.text_input("Название автомобиля")
    fuel_type = st.selectbox("Тип топлива", ["Бензин", "Дизель", "Электро", "Гибрид"])
    transmission_type = st.selectbox("Коробка передач", ["Механика", "Автомат"])
    rental_cost_per_day = st.number_input("Стоимость аренды в день (руб.)", min_value=0.0, step=0.01, format="%.2f")

    fleets = service.get_fleets()
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

            service.add_car(
                name=car_name,
                fuel_type=fuel_type,
                transmission_type=transmission_type,
                rental_cost_per_day=rental_cost_per_day,
                fleet_id=fleet_choices[selected_fleet],
            )

            st.success("Автомобиль успешно добавлен!")
        except Exception as e:
            st.error(f"Ошибка: {e}")
