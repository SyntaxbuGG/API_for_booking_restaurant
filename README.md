# 🍽️ Restaurant Table Reservation API

API-сервис для бронирования столиков в ресторане, реализованный на FastAPI. Поддерживает создание, просмотр и удаление броней, управление столиками и проверку доступности по времени.

## 🚀 Технологии

- [FastAPI](https://fastapi.tiangolo.com/) — веб-фреймворк
- [PostgreSQL](https://www.postgresql.org/) — база данных
- [SQLAlchemy](https://www.sqlalchemy.org/) / [SQLModel](https://sqlmodel.tiangolo.com/) — ORM
- [Alembic](https://alembic.sqlalchemy.org/) — миграции
- [Docker](https://www.docker.com/) + [docker-compose](https://docs.docker.com/compose/) — контейнеризация
- [Pytest](https://docs.pytest.org/) — тестирование (опционально)

---

## 📦 Функционал

### 🔹 Модель Table (столик)
| Поле | Тип | Описание |
|------|-----|----------|
| `id` | int | Уникальный идентификатор |
| `name` | str | Название столика (например, "Table 1") |
| `seats` | int | Количество мест |
| `location` | str | Местоположение (например, "зал у окна") |

### 🔹 Модель Reservation (бронь)
| Поле | Тип | Описание |
|------|-----|----------|
| `id` | int | Уникальный идентификатор |
| `customer_name` | str | Имя клиента |
| `table_id` | int | Идентификатор столика |
| `reservation_time` | datetime | Время начала брони |
| `duration_minutes` | int | Продолжительность брони в минутах |

---

## 🛠️ Методы API

### 📋 Столики:
- `GET /tables/` — список всех столиков
- `POST /tables/` — создать новый столик
- `DELETE /tables/{id}` — удалить столик

### 📋 Брони:
- `GET /reservations/` — список всех броней
- `POST /reservations/` — создать новую бронь
- `DELETE /reservations/{id}` — удалить бронь

📌 **Бизнес-логика**:
- Нельзя создать бронь, если в указанный временной слот столик уже занят.
- Конфликт бронирования возвращает понятное сообщение об ошибке.

---

## ⚙️ Установка и запуск

### 1. Клонировать репозиторий
```
bash
git clone https://github.com/SyntaxbuGG/API_for_booking_restaurant.git .

### 2. Запустить проект с помощью Docker
bash
docker-compose up --build

### 3. Активировать миграции alembic вручную в первый раз после запуска docker 
bash 
docker-compose exec app alembic revision --autogenerate -m "Initial tables"
docker-compose exec app alembic upgrade head

```
## Пример запроса на создание брони
```http
POST /reservations/
Content-Type: application/json

{
  "customer_name": "John Doe",
  "table_id": 1,
  "reservation_time": "2025-04-12T18:00:00",
  "duration_minutes": 90
}
```
## Остановка проекта
bash
docker-compose down -v 

## 🗂 Структура проекта

```bash
restaurant_reservation/
├── alembic/              # Миграции базы данных
├── app/
│   ├── models/           # SQLAlchemy модели
│   ├── schemas/          # Pydantic схемы (DTO)
│   ├── services/         # Бизнес-логика
│   ├── routers/          # FastAPI эндпоинты
│   ├── database.py       # Подключение к PostgreSQL
│   └── main.py           # Запуск приложения
├── tests/                # Pytest тесты
├── Dockerfile            # Образ для Docker
├── docker-compose.yml    # Конфигурация сервисов
├── requirements.txt      # Зависимости
└── README.md            # Документация
```

👨‍💻 Автор
```
Сделано в рамках тестового задания
GitHub: SyntaxbuGG
```
