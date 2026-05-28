# Django Backend для «РукоДел»

Полноценный backend на Django с REST API для интернет-магазина ручных изделий.

## 📋 Структура проекта

```
rukodel/
├── manage.py                 # Утилита управления Django
├── requirements.txt          # Зависимости Python
├── schema.sql               # SQL-схема БД для MySQL
├── .env.example             # Пример файла с переменными окружения
│
├── rukodel/                 # Главная папка проекта
│   ├── __init__.py
│   ├── settings.py          # Настройки Django
│   ├── urls.py              # Главные URL-маршруты
│   ├── wsgi.py              # WSGI конфигурация
│   └── asgi.py              # ASGI конфигурация
│
└── shop/                    # Приложение магазина
    ├── __init__.py
    ├── apps.py              # Конфигурация приложения
    ├── models.py            # Модели БД (ORM)
    ├── views.py             # Представления (ViewSets)
    ├── serializers.py       # Сериализаторы REST API
    ├── urls.py              # URL-маршруты API
    └── admin.py             # Настройки админ-панели
```

## 🗄️ Модели базы данных

### User (Пользователи)
- Расширенная модель пользователя Django
- Роли: `buyer` (покупатель), `master` (мастер), `admin`
- Поля: username, email, password, role, phone, created_at

### Master (Мастера)
- Профиль мастера (продавца)
- Связь: OneToOne с User
- Поля: specialty, description, avatar, rating

### Category (Категории)
- Категории товаров
- Поля: name, slug, description

### Product (Товары)
- Изделия ручной работы
- Связи: ForeignKey к Master и Category
- Поля: name, description, price, quantity, image, is_active

### Order (Заказы)
- Заказы покупателей
- Связь: ForeignKey к User
- Поля: total_price, status, delivery_address, comment
- Статусы: pending, processing, shipped, delivered, cancelled

### OrderItem (Позиции заказа)
- Товары в заказе
- Связи: ForeignKey к Order и Product
- Поля: quantity, price

### Cart (Корзина)
- Корзина покупателя
- Связи: ForeignKey к User и Product
- Поля: quantity

### Review (Отзывы)
- Отзывы о товарах
- Связи: ForeignKey к Product и User
- Поля: rating (1-5), comment

## 🚀 Установка и запуск

### 1. Создание виртуального окружения

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Создание базы данных MySQL

```bash
# Войти в MySQL
mysql -u root -p

# Создать БД и пользователя
CREATE DATABASE rukodel CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'rukodel_app'@'localhost' IDENTIFIED BY 'YourPassword';
GRANT ALL PRIVILEGES ON rukodel.* TO 'rukodel_app'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Применить SQL-схему (опционально, Django создаст таблицы сам)
mysql -u rukodel_app -p rukodel < schema.sql
```

### 4. Настройка переменных окружения

```bash
# Скопировать пример
cp .env.example .env

# Отредактировать .env и указать реальные данные
```

### 5. Миграции Django

```bash
# Создать миграции
python manage.py makemigrations

# Применить миграции
python manage.py migrate
```

### 6. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 7. Запуск сервера

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: `http://localhost:8000`

## 📡 REST API Endpoints

### Аутентификация
- `POST /api-auth/login/` — Вход
- `POST /api-auth/logout/` — Выход

### Пользователи
- `GET /api/users/` — Список пользователей
- `POST /api/users/` — Регистрация
- `GET /api/users/me/` — Текущий пользователь
- `GET /api/users/{id}/` — Детали пользователя

### Мастера
- `GET /api/masters/` — Список мастеров
- `GET /api/masters/{id}/` — Детали мастера

### Категории
- `GET /api/categories/` — Список категорий
- `GET /api/categories/{slug}/` — Категория по slug

### Товары
- `GET /api/products/` — Список товаров
- `GET /api/products/{id}/` — Детали товара
- `POST /api/products/` — Создать товар (для мастеров)
- `PUT /api/products/{id}/` — Обновить товар
- `DELETE /api/products/{id}/` — Удалить товар

**Фильтры товаров:**
- `?category=keramika` — По категории (slug)
- `?master=1` — По мастеру (ID)
- `?in_stock=true` — Только в наличии
- `?min_price=1000&max_price=5000` — Ценовой диапазон
- `?search=ваза` — Поиск по названию/описанию
- `?ordering=-created_at` — Сортировка

### Корзина
- `GET /api/cart/` — Содержимое корзины
- `POST /api/cart/` — Добавить в корзину
- `PUT /api/cart/{id}/` — Обновить количество
- `DELETE /api/cart/{id}/` — Удалить из корзины
- `DELETE /api/cart/clear/` — Очистить корзину
- `GET /api/cart/total/` — Общая сумма

### Заказы
- `GET /api/orders/` — Список заказов
- `POST /api/orders/` — Создать заказ из корзины
- `GET /api/orders/{id}/` — Детали заказа
- `PATCH /api/orders/{id}/` — Обновить статус (для админа)

### Отзывы
- `GET /api/reviews/` — Список отзывов
- `POST /api/reviews/` — Добавить отзыв
- `GET /api/reviews/{id}/` — Детали отзыва

## 🔒 Администраторская панель

Доступна по адресу: `http://localhost:8000/admin/`

Возможности:
- Управление пользователями
- Управление товарами и категориями
- Просмотр и обработка заказов
- Управление мастерами
- Просмотр отзывов

## 🛠️ Примеры использования API

### Регистрация пользователя

```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "ivan",
    "email": "ivan@example.com",
    "password": "securepass123",
    "first_name": "Иван",
    "last_name": "Иванов",
    "role": "buyer"
  }'
```

### Получение списка товаров

```bash
curl http://localhost:8000/api/products/?category=keramika&in_stock=true
```

### Добавление товара в корзину

```bash
curl -X POST http://localhost:8000/api/cart/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -d '{
    "product": 1,
    "quantity": 2
  }'
```

### Создание заказа

```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -d '{
    "delivery_address": "Москва, ул. Ленина, д.1, кв.10",
    "comment": "Позвоните перед доставкой"
  }'
```

## 📊 SQL-схема

Полная SQL-схема находится в файле `schema.sql` и включает:
- Таблицы с индексами и внешними ключами
- Представления (VIEWS) для аналитики:
  - `popular_products` — Популярные товары
  - `masters_stats` — Статистика по мастерам
- Хранимые процедуры:
  - `update_master_rating()` — Обновление рейтинга мастера
  - `get_products_by_category()` — Товары по категории
- Триггеры для автоматического обновления рейтингов

## 🧪 Тестирование

```bash
# Запуск тестов
python manage.py test

# Создание тестовых данных
python manage.py loaddata fixtures/test_data.json
```

## 📦 Деплой

### Настройки для продакшена

1. Установить `DEBUG=False` в `.env`
2. Настроить `ALLOWED_HOSTS`
3. Использовать реальный `SECRET_KEY`
4. Настроить веб-сервер (nginx + gunicorn)
5. Настроить HTTPS
6. Настроить статические файлы:

```bash
python manage.py collectstatic
```

### Пример конфигурации gunicorn

```bash
gunicorn rukodel.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

## 📝 Лицензия

Этот проект создан в учебных целях для демонстрации работы Django с MySQL.

## 💡 Полезные команды

```bash
# Создать миграции
python manage.py makemigrations

# Применить миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Запустить сервер
python manage.py runserver

# Запустить shell
python manage.py shell

# Собрать статические файлы
python manage.py collectstatic

# Создать дамп БД
python manage.py dumpdata > backup.json

# Загрузить дамп
python manage.py loaddata backup.json
```
