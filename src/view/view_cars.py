import streamlit as st
from services.rental_service import RentalService
from services.auth_service import AuthService
from services.payment_service import PaymentService
import re


def Cars():
    st.title("Аренда автомобиля")
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Cars"

    if st.session_state.current_page == "rent_car":
        render_rent_car_page()
    elif st.session_state.current_page == "payment":
        render_payment_page()
    else:
        render_view_cars_page()


def render_view_cars_page():

    rental_service = RentalService()

    cities = rental_service.get_cities()
    fleets = rental_service.get_fleets()

    selected_city = st.selectbox("Выберите город", options=cities)

    available_fleets = [fleet for fleet in fleets if fleet[2] == selected_city] 

    if not available_fleets:
        st.error("В выбранном городе нет доступных автопарков.")
        return

    selected_fleet = st.selectbox(
        "Выберите автопарк", 
        options=[fleet[1] for fleet in available_fleets]  
    )
    fleet_id = next(fleet[0] for fleet in available_fleets if fleet[1] == selected_fleet)  

    available_cars = rental_service.get_available_cars()
    cars_in_fleet = [car for car in available_cars if car['fleet_id'] == fleet_id]

    if not cars_in_fleet:
        st.error("В выбранном автопарке нет доступных машин.")
        return

    st.write("Доступные автомобили:")
    for car in cars_in_fleet:
        st.markdown(f"**Модель**: {car['name']}")
        st.markdown(f"**Тип топлива**: {car['fuel_type']}")
        st.markdown(f"**Тип коробки передач**: {car['transmission_type']}")
        st.markdown(f"**Стоимость аренды в день**: {car['rental_cost_per_day']} руб.")

        if st.button("Арендовать", key=f"rent_{car['car_id']}"):
            st.session_state.selected_car = car
            st.session_state.current_page = "rent_car"
            st.rerun()

        st.markdown("---")


def render_rent_car_page():
    st.title("Оформление аренды автомобиля")

    if "user_id" not in st.session_state:
        st.error("Вы не авторизованы.")
        return

    rental_service = RentalService()
    auth_service = AuthService()

    documents = auth_service.get_documents(st.session_state.user_id)
    passport = documents.get("passport")
    if not(isinstance(passport, dict) and all(passport.values())):            
        st.error("Для аренды автомобиля необходимо добавить паспортные данные.")
        return

    driver_license = documents.get("driverLicenses")
    if not (isinstance(passport, dict) and all(passport.values())):            
        st.error("Для аренды автомобиля необходимо добавить данные водительских прав.")
        return
    
    if "selected_car" not in st.session_state:
        st.error("Сначала выберите автомобиль для аренды на странице выбора.")
        st.sessiob_state.current_page = "Cars"
        st.rerun()

    selected_car = st.session_state.selected_car

    st.markdown(f"### Выбранный автомобиль: {selected_car['name']}")
    st.markdown(f"**Тип топлива**: {selected_car['fuel_type']}")
    st.markdown(f"**Тип трансмиссии**: {selected_car['transmission_type']}")
    st.markdown(f"**Стоимость аренды в день**: {selected_car['rental_cost_per_day']} руб.")
    st.markdown("---")

    start_date = st.date_input("Дата начала аренды")
    end_date = st.date_input("Дата окончания аренды")

    if start_date >= end_date:
        st.error("Дата окончания должна быть позже даты начала.")
        return

    if st.button("Подтвердить аренду"):
        try:
            user_id = st.session_state.user_id
            car_id = selected_car["car_id"]
            rental_id = rental_service.add_rental(user_id, car_id, str(start_date), str(end_date))
            st.success("Аренда успешно оформлена! Теперь перейдите к оплате.")
            st.session_state.rental_id = rental_id
            st.session_state.selected_car = None

            st.session_state.current_page = 'payment'
            st.rerun()
        except Exception as e:
            st.error(f"Ошибка при оформлении аренды: {str(e)}")

def render_payment_page():
    st.title("Оплата аренды автомобиля")

    if "user_id" not in st.session_state:
        st.error("Ошибка: пользователь не авторизован.")
        return

    
    if "rental_id" not in st.session_state:
        st.error("Ошибка: аренда не найдена.")
        return

    rental_id = st.session_state.rental_id
    rental_service = RentalService()
    rental_info = rental_service.get_rental_by_id(rental_id)

    amount = rental_info['total_price']

    st.write(f"Машина: {rental_info['car_name']}")
    st.write(f"Стоимость аренды: {rental_info['total_price']} руб.")

    card_number = st.text_input("Введите номер карты")
    card_expiry = st.text_input("Введите срок действия карты (MM/YY)")
    card_cvc = st.text_input("Введите CVC")

    if card_number and not re.match(r"^\d{16}$", card_number):
        st.error("Номер карты должен содержать 16 цифр.")
        return

    if card_expiry and not re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", card_expiry):
        st.error("Срок действия карты должен быть в формате MM/YY.")
        return

    if card_cvc and not re.match(r"^\d{3}$", card_cvc):
        st.error("CVC код должен содержать 3 цифры.")
        return

    if st.button("Оплатить"):
        if not card_number or not card_expiry or not card_cvc:
            st.error("Пожалуйста, заполните все поля.")
            return

        payment_service = PaymentService()
        try:
            payment_id = payment_service.create_payment(
                rental_id=rental_id,
                amount=amount,
                card_number=card_number,
                card_expiry=card_expiry,
                card_cvc=card_cvc
            )
            payment_service.update_payment_status(payment_id, 'Оплачено')
            st.success("Оплата прошла успешно!")

            st.session_state.page = "Cars"
            st.rerun()
        except Exception as e:
            st.error(f"Ошибка при оплате: {str(e)}")
