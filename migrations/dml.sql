-- Вставка данных в таблицу автопарков
INSERT INTO fleets (name, address, city) 
VALUES 
    ('Центральный автопарк', 'ул. Ленина, д. 1','Москва'),
    ('Северный автопарк', 'ул. Невский, д. 25','Санкт-Петербург'),
    ('Южный автопарк', 'ул. Курортная, д. 10', 'Сочи');

-- Вставка данных в таблицу пользователей
INSERT INTO users (name, email, password_hash, role) 
VALUES 
    ('Иван', 'ivan.petrov@example.com', '$2b$12$WWivymLjMT2MYLQxwY7UsOuU21u52rbPckBK1XB5guOQUC/FlQ0Uu', 'admin'),
    ('Мария', 'maria.ivanova@example.com', '$2b$12$1eQRCLcl0QfQ2jUunoHVx.hLwV.zaPiB8NtaP8k9b6nEBWmjsuMbO', 'user'),
    ('Red', 'red@mail.ru', '$2b$12$2ndnvKoaCnJnscivmDy.mOHbvVDTOHhEW4oIen60nq12S5.7C2a3K', 'admin');

-- Вставка данных в таблицу машин
INSERT INTO cars (name, fuel_type, transmission_type, rental_cost_per_day, fleet_id) 
VALUES
    ('Toyota Corolla', 'Gasoline', 'Automatic', 3500.00, 1),
    ('Honda Civic', 'Gasoline', 'Manual', 3000.00, 1),
    ('Tesla Model 3', 'Electric', 'Automatic', 5000.00, 2),
    ('Ford Focus', 'Diesel', 'Manual', 2500.00, 3),
    ('Chevrolet Bolt', 'Electric', 'Automatic', 4000.00, 2);