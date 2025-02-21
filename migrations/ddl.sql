-- Таблица для хранения информации об автопарках
CREATE TABLE fleets (
    fleet_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL
);

COMMENT ON TABLE fleets IS 'Информация об автопарках';
COMMENT ON COLUMN fleets.fleet_id IS 'Уникальный идентификатор автопарка';
COMMENT ON COLUMN fleets.name IS 'Название автопарка';
COMMENT ON COLUMN fleets.address IS 'Адрес';
COMMENT ON COLUMN fleets.city IS 'Название города';

-- Таблица для хранения информации о машинах
CREATE TABLE cars (
    car_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    fuel_type VARCHAR(50) NOT NULL,
    transmission_type VARCHAR(50) NOT NULL,
    rental_cost_per_day DECIMAL(10, 2) NOT NULL,
    fleet_id INT NOT NULL,
    FOREIGN KEY (fleet_id) REFERENCES fleets(fleet_id) ON DELETE CASCADE
);

COMMENT ON TABLE cars IS 'Информация о машинах';
COMMENT ON COLUMN cars.car_id IS 'Уникальный идентификатор машины';
COMMENT ON COLUMN cars.name IS 'Название машины';
COMMENT ON COLUMN cars.fuel_type IS 'Вид топлива';
COMMENT ON COLUMN cars.transmission_type IS 'Вид коробки передач';
COMMENT ON COLUMN cars.rental_cost_per_day IS 'Стоимость аренды за один день';
COMMENT ON COLUMN cars.fleet_id IS 'Идентификатор автопарка';

-- Таблица для хранения информации о пользователях
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'admin'))
);

COMMENT ON TABLE users IS 'Информация о пользователях';
COMMENT ON COLUMN users.user_id IS 'Уникальный идентификатор пользователя';
COMMENT ON COLUMN users.name IS 'Имя пользователя';
COMMENT ON COLUMN users.email IS 'Почта пользователя';
COMMENT ON COLUMN users.password_hash IS 'Хеш пароля пользователя';
COMMENT ON COLUMN users.role IS 'Роль пользователя (например, "admin", "user")';

-- Таблица для хранения информации о паспортах
CREATE TABLE passports (
    passport_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    mid_name VARCHAR(100),
    passport_series VARCHAR(10) NOT NULL,
    passport_number VARCHAR(20) NOT NULL,
    birth_date DATE NOT NULL,                     
    issue_date DATE NOT NULL,                     
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

COMMENT ON TABLE passports IS 'Информация о паспортах';
COMMENT ON COLUMN passports.passport_id IS 'Уникальный идентификатор паспорта';
COMMENT ON COLUMN passports.user_id IS 'Идентификатор пользователя';
COMMENT ON COLUMN passports.first_name IS 'Имя человека';
COMMENT ON COLUMN passports.last_name IS 'Фамилия человека';
COMMENT ON COLUMN passports.mid_name IS 'Отчество человека';
COMMENT ON COLUMN passports.passport_series IS 'Серия паспорта';
COMMENT ON COLUMN passports.passport_number IS 'Номер паспорта';
COMMENT ON COLUMN passports.birth_date IS 'Дата рождения';
COMMENT ON COLUMN passports.issue_date IS 'Дата выдачи паспорта';

CREATE TABLE driverLicenses (
    license_id SERIAL PRIMARY KEY,                 
    user_id INT NOT NULL,                        
    license_number VARCHAR(20) NOT NULL UNIQUE,    
    issue_date DATE NOT NULL,                     
    expiration_date DATE NOT NULL,                 
    issuing_authority VARCHAR(100) NOT NULL,  
    category VARCHAR(10) NOT NULL,                     
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

COMMENT ON TABLE driverLicenses IS 'Информация о водительских правах';
COMMENT ON COLUMN driverLicenses.license_id IS 'Уникальный идентификатор водительских прав';
COMMENT ON COLUMN driverLicenses.user_id IS 'Идентификатор владельца водительских прав';
COMMENT ON COLUMN driverLicenses.license_number IS 'Уникальный номер водительских прав';
COMMENT ON COLUMN driverLicenses.issue_date IS 'Дата выдачи водительских прав';
COMMENT ON COLUMN driverLicenses.expiration_date IS 'Дата истечения срока действия водительских прав';
COMMENT ON COLUMN driverLicenses.issuing_authority IS 'Орган, выдавший права';
COMMENT ON COLUMN driverLicenses.category IS 'Категория водительских прав';

-- Таблица для хранения информации об арендах
CREATE TABLE rentals (
    rental_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    car_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('active', 'completed')),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (car_id) REFERENCES cars(car_id) ON DELETE CASCADE
);

COMMENT ON TABLE rentals IS 'Информация об арендах';
COMMENT ON COLUMN rentals.rental_id IS 'Уникальный идентификатор аренды';
COMMENT ON COLUMN rentals.user_id IS 'Идентификатор пользователя';
COMMENT ON COLUMN rentals.car_id IS 'Идентификатор машины';
COMMENT ON COLUMN rentals.start_date IS 'Дата началы аренды';
COMMENT ON COLUMN rentals.end_date IS 'Дата окончания аренды';
COMMENT ON COLUMN rentals.status IS 'Статус аренды';

-- Таблица для хранения информации о платежах
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    rental_id INT NOT NULL UNIQUE,
    payment_date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    card_number VARCHAR(20) NOT NULL,
    card_expiry VARCHAR(7) NOT NULL,
    card_cvc VARCHAR(4) NOT NULL,
    FOREIGN KEY (rental_id) REFERENCES rentals(rental_id) ON DELETE CASCADE
);

COMMENT ON TABLE payments IS 'Информация об платежах';
COMMENT ON COLUMN payments.rental_id IS 'Уникальный идентификатор платежа';
COMMENT ON COLUMN payments.rental_id IS 'Идентификатор аренды';
COMMENT ON COLUMN payments.payment_date IS 'Дата оплаты';
COMMENT ON COLUMN payments.amount IS 'Сумма платежа';
COMMENT ON COLUMN payments.status IS 'Статус платежа';
COMMENT ON COLUMN payments.card_number IS 'Номер карты';
COMMENT ON COLUMN payments.card_expiry IS 'Срок действия карты';
COMMENT ON COLUMN payments.card_cvc IS 'CVC';