import streamlit as st
from services.auth_service import AuthService

def profile():
    st.title("Профиль пользователя")
    
    if "user_id" not in st.session_state:
        st.error("Вы не авторизованы.")
        return

    if "current_page" not in st.session_state:
        st.session_state.current_page = "profile"

    if st.session_state.current_page == "add_passport":
        render_add_passport_page()
    elif st.session_state.current_page == "add_driver_license":
        render_add_driver_license_page()
    else:
        render_profile_page()

def render_profile_page():
    user_service = AuthService()
    try:
        documents = user_service.get_documents(st.session_state.user_id)
        st.subheader("Документы")
            
        passport = documents.get("passport")
        if isinstance(passport, dict) and all(passport.values()):            
            st.write("### Паспорт")
            st.write(f"**ФИО:** {passport['last_name']} {passport['first_name']} {passport['mid_name']}")
            st.write(f"**Серия:** {passport['passport_series']}")
            st.write(f"**Номер:** {passport['passport_number']}")
            st.write(f"**Дата рождения:** {passport['birth_date']}")
            st.write(f"**Дата выдачи:** {passport['issue_date']}")
        else:
            st.warning("Паспортные данные отсутствуют.")
            if st.button("Добавить паспортные данные"):
                st.session_state.current_page = "add_passport"
                st.rerun()

        driver_license = documents.get("driverLicenses")
        if isinstance(driver_license, dict) and all(driver_license.values()):            
            st.write("### Водительское удостоверение")
            st.write(f"**Номер:** {driver_license['license_number']}")
            st.write(f"**Дата выдачи:** {driver_license['issue_date']}")
            st.write(f"**Срок действия до:** {driver_license['expiration_date']}")
            st.write(f"**Орган:** {driver_license['issuing_authority']}")
            st.write(f"**Категория:** {driver_license['category']}")

        else:
            st.warning("Данные водительских прав отсутствуют.")
            if st.button("Добавить данные водительских прав"):
                st.session_state.current_page = "add_driver_license"
                st.rerun()
    except Exception as e:
        st.error(f"Ошибка загрузки профиля: {str(e)}")


def render_add_passport_page():
    st.title("Добавление паспорта")

    if "passport_form" not in st.session_state:
        st.session_state.passport_form = {
            "last_name": "",
            "first_name": "",
            "mid_name": "",
            "passport_series": "",
            "passport_number": "",
            "birth_date": None,
            "issue_date": None,
        }

    form = st.session_state.passport_form
    form["last_name"] = st.text_input("Фамилия", value=form["last_name"])
    form["first_name"] = st.text_input("Имя", value=form["first_name"])
    form["mid_name"] = st.text_input("Отчество", value=form["mid_name"])
    form["passport_series"] = st.text_input("Серия паспорта", value=form["passport_series"])
    form["passport_number"] = st.text_input("Номер паспорта", value=form["passport_number"])
    form["birth_date"] = st.date_input("Дата рождения", value=form["birth_date"])
    form["issue_date"] = st.date_input("Дата выдачи", value=form["issue_date"])


    if st.button("Сохранить"):
        user_service = AuthService()
        user_service.add_passport(
            user_id=st.session_state.user_id,
            first_name=form["first_name"],
            last_name=form["last_name"],
            mid_name=form["mid_name"],
            passport_serires=form["passport_series"],
            passport_number=form["passport_number"],
            birth_date=str(form["birth_date"]),
            issue_date=str(form["issue_date"])
        )
        st.success("Паспорт успешно добавлен!")
        st.session_state.current_page = "profile"
        st.rerun()

    if st.button("Отмена"):
        st.session_state.current_page = "profile"
        st.rerun()


def render_add_driver_license_page():
    st.title("Добавление водительских прав")

    if "driver_license_form" not in st.session_state:
        st.session_state.driver_license_form = {
            "license_number": "",
            "issue_date": None,
            "expiration_date": None,
            "issuing_authority": "",
            "category": "",
        }

    form = st.session_state.driver_license_form
    form["license_number"] = st.text_input("Номер водительского удостоверения", value=form["license_number"])
    form["issue_date"] = st.date_input("Дата выдачи", value=form["issue_date"])
    form["expiration_date"] = st.date_input("Срок действия до", value=form["expiration_date"])
    form["issuing_authority"] = st.text_input("Орган, выдавший права", value=form["issuing_authority"])
    form["category"] = st.text_input("Категория", value=form["category"])

    if st.button("Сохранить"):
        user_service = AuthService()
        user_service.add_driver_license(
            user_id=st.session_state.user_id,
            license_number=form["license_number"],
            issue_date=str(form["issue_date"]),
            expiration_date=str(form["expiration_date"]),
            issuing_authority=form["issuing_authority"],
            category=form["category"]
        )
        st.success("Водительское удостоверение успешно добавлено!")
        st.session_state.current_page = "profile"
        st.rerun()

    if st.button("Отмена"):
        st.session_state.current_page = "profile"
        st.rerun()
