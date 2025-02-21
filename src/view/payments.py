import streamlit as st
from services.rental_service import RentalService


def render_your_rentels():
    st.title("Ваши аренды и платежи")

    if "user_id" not in st.session_state:
        st.error("Вы не авторизованы.")
        return
    rental_service = RentalService()

    rentals = rental_service.get_rentals_by_user(st.session_state.user_id) 

    if not rentals:
        st.info("У вас пока нет аренд.")
        return

    st.header("Текущие аренды")

    active_rentals = [rental for rental in rentals if rental['status'] == 'active']
    if active_rentals:
        for rental in active_rentals:
            st.subheader(f"Аренда")
            st.write(f"Машина: {rental['car_name']}")
            st.write(f"Дата начала: {rental['start_date']}")
            st.write(f"Дата окончания: {rental['end_date']}")
            st.write(f"Автопарк: {rental['fleet_name']}")
            st.write(f"Адрес автопарка: {rental['fleet_address']}")
            st.write(f"Город: {rental['city']}")
            st.write(f"Сумма платежа: {rental['payment_amount']} руб.")
            st.write(f"Статус: {rental['status']}")
            st.markdown("---")
    else:
        st.write("У вас нет активных аренд.")

    st.header("Завершённые аренды")

    completed_rentals = [rental for rental in rentals if rental['status'] == 'completed']
    if completed_rentals:
        for rental in completed_rentals:
            st.subheader(f"Аренда ID: {rental['rental_id']}")
            st.write(f"Машина: {rental['car_name']}")
            st.write(f"Дата начала: {rental['start_date']}")
            st.write(f"Дата окончания: {rental['end_date']}")
            st.write(f"Статус: {rental['status']}")
            st.markdown("---")
    else:
        st.write("У вас нет завершённых аренд.")
