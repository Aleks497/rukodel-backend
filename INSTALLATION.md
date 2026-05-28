# 🚀 Инструкция по установке Django backend для «РукоДел»

## 📋 Шаг 1: Создание структуры проекта

Создайте на вашем компьютере следующую структуру папок:

```
rukodel-backend/
├── manage.py
├── requirements.txt
├── schema.sql
├── .env.example
├── README_DJANGO.md
├── rukodel/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── shop/
    ├── __init__.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── serializers.py
    ├── urls.py
    └── admin.py
```

## 📥 Шаг 2: Скопировать файлы

**Вариант A:** Скачайте все файлы из окна предпросмотра (кнопка скачивания вверху справа)

**Вариант B:** Скопируйте содержимое каждого файла вручную из предпросмотра и создайте файлы локально

## 💻 Шаг 3: Установка зависимостей

### 3.1. Убедитесь, что у вас установлены:
- **Python 3.8+** (проверить: `python --version`)
- **MySQL 8.0+** или **MariaDB 10.5+** (проверить: `mysql --version`)
- **pip** (проверить: `pip --version`)

### 3.2. Создайте виртуальное окружение

#### Windows:
```bash
cd rukodel-backend
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS:
```bash
cd rukodel-backend
python3 -m venv venv
source venv/bin/activate
```

### 3.3. Установите зависимости

```bash
pip install -r requirements.txt
```

**Если получаете ошибку с `mysqlclient` на Windows:**

```bash
# Установите предварительно скомпилированный пакет
pip install mysqlclient-1.4.6-cp310-cp310-win_amd64.whl

# Или используйте PyMySQL:
pip install PyMySQL
```

Затем в `rukodel/settings.py` добавьте в самом начале:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

## 🗄️ Шаг 4: Настройка MySQL базы данных

### 4.1. Войдите в MySQL

```bash
mysql -u root -p
```

### 4.2. Создайте базу данных и пользователя

```sql
CREATE DATABASE rukodel CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'rukodel_app'@'localhost' IDENTIFIED BY 'YourStrongPassword123';

GRANT ALL PRIVILEGES ON rukodel.* TO 'rukodel_app'@'localhost';

FLUSH PRIVILEGES;

EXIT;
```

### 4.3. (Опционально) Применить готовую SQL-схему

```bash
mysql -u rukodel_app -p rukodel < schema.sql
```

**Или** пропустите этот шаг — Django создаст таблицы сам при миграции.

## ⚙️ Шаг 5: Настройка переменных окружения

### 5.1. Создайте файл `.env`

```bash
cp .env.example .env
```

### 5.2. Отредактируйте `.env`

Откройте файл `.env` и укажите реальные данные:

```
SECRET_KEY=your-secret-key-here-generate-random-string
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=rukodel
DB_USER=rukodel_app
DB_PASSWORD=YourStrongPassword123
DB_HOST=localhost
DB_PORT=3306
```

**Как сгенерировать SECRET_KEY:**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 🔧 Шаг 6: Применение миграций Django

### 6.1. Создайте миграции

```bash
python manage.py makemigrations
```

### 6.2. Примените миграции

```bash
python manage.py migrate
```

Эта команда создаст все таблицы в БД автоматически.

## 👤 Шаг 7: Создание суперпользователя (администратора)

```bash
python manage.py createsuperuser
```

Введите:
- Username: `admin`
- Email: `admin@rukodel.ru`
- Password: (ваш пароль)

## 🚀 Шаг 8: Запуск сервера

```bash
python manage.py runserver
```

Сервер запустится на `http://localhost:8000`

## ✅ Проверка работы

### Админ-панель:
Откройте в браузере: `http://localhost:8000/admin/`
Войдите с данными суперпользователя.

### API:
- `http://localhost:8000/api/products/` — список товаров
- `http://localhost:8000/api/categories/` — категории
- `http://localhost:8000/api/masters/` — мастера

## 🛠️ Полезные команды

```bash
# Создать тестовые данные
python manage.py shell
>>> from shop.models import Category
>>> Category.objects.create(name="Керамика", slug="keramika")
>>> Category.objects.create(name="Текстиль", slug="textil")
>>> exit()

# Просмотреть все таблицы БД
python manage.py dbshell
mysql> SHOW TABLES;
mysql> EXIT;

# Создать дамп БД
mysqldump -u rukodel_app -p rukodel > backup.sql

# Остановить сервер
Ctrl + C
```

## 🐛 Решение проблем

### Ошибка: "No module named 'shop'"

```bash
# Убедитесь, что находитесь в правильной директории
cd rukodel-backend
python manage.py runserver
```

### Ошибка: "Access denied for user"

Проверьте данные в `.env` файле:
- Правильный пароль
- Пользователь создан в MySQL
- Права выданы

### Ошибка: "mysqlclient" не устанавливается

**Windows:**
```bash
pip install PyMySQL
```

И добавьте в `rukodel/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

**Linux:**
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient
```

**macOS:**
```bash
brew install mysql
pip install mysqlclient
```

## 📞 Дальнейшие шаги

1. ✅ Создайте категории через админ-панель
2. ✅ Создайте профили мастеров
3. ✅ Добавьте товары
4. ✅ Протестируйте API через браузер или Postman
5. ✅ Подключите frontend (index.html) к API

## 🎉 Готово!

Теперь у вас запущен Django backend с MySQL для сайта «РукоДел»!
