# 🐍 Установка проекта Django "РукоДел" в PyCharm

## Способ 1: Автоматическая установка (РЕКОМЕНДУЕТСЯ)

### Шаг 1: Скачать установочный скрипт

1. В окне предпросмотра справа найдите файл **`setup_project.py`**
2. Нажмите на него правой кнопкой → **Скачать** (или используйте кнопку Download вверху)
3. Сохраните файл на компьютере (например, на Рабочий стол)

### Шаг 2: Запустить установщик

Откройте командную строку (cmd) или PowerShell и выполните:

```bash
# Перейдите в папку, где сохранён setup_project.py
cd Desktop

# Запустите установщик
python setup_project.py
```

Установщик создаст папку `rukodel-backend` со всей структурой проекта.

### Шаг 3: Скопировать недостающие файлы

Скопируйте из **окна предпросмотра** содержимое следующих файлов в созданную папку `rukodel-backend`:

**Обязательные файлы для копирования:**

1. **`shop/models.py`** — Модели базы данных
2. **`shop/views.py`** — REST API views
3. **`shop/serializers.py`** — Сериализаторы
4. **`shop/admin.py`** — Админ-панель
5. **`shop/urls.py`** — URL маршруты
6. **`schema.sql`** — SQL схема

**Как скопировать:**
- Откройте файл в предпросмотре справа
- Выделите ВСЁ содержимое (Ctrl+A)
- Скопируйте (Ctrl+C)
- Создайте файл в проекте с тем же именем
- Вставьте содержимое (Ctrl+V)
- Сохраните (Ctrl+S)

---

## Способ 2: Ручная установка (если автоматический не работает)

### Шаг 1: Скачать все файлы

В окне предпросмотра справа нажмите кнопку **"Download"** (⬇️) вверху — это скачает ВСЕ файлы проекта одним архивом.

### Шаг 2: Распаковать архив

Распакуйте скачанный ZIP-архив в любую папку, например:
```
C:\Users\YourName\Projects\rukodel-backend
```

---

## 🔧 Открытие проекта в PyCharm

### Шаг 1: Открыть проект

1. Запустите **PyCharm**
2. Выберите **File → Open**
3. Найдите папку **`rukodel-backend`** и откройте её
4. Выберите **"Open as Project"**

### Шаг 2: Настроить интерпретатор Python

1. В PyCharm откройте: **File → Settings** (Ctrl+Alt+S)
2. Перейдите: **Project: rukodel-backend → Python Interpreter**
3. Нажмите на **⚙️ (шестерёнку)** → **Add Interpreter** → **Add Local Interpreter**
4. Выберите **Virtualenv Environment**
5. Выберите **New environment**
6. Location: оставьте по умолчанию (будет создана папка `venv` в проекте)
7. Base interpreter: выберите Python 3.8 или выше
8. Нажмите **OK**

PyCharm автоматически создаст виртуальное окружение.

### Шаг 3: Установить зависимости

В PyCharm откройте **Terminal** (Alt+F12) внизу и выполните:

```bash
pip install -r requirements.txt
```

**Если возникает ошибка с `mysqlclient`:**

```bash
pip install Django djangorestframework django-cors-headers PyMySQL python-dotenv Pillow
```

---

## 🗄️ Настройка базы данных MySQL

### Шаг 1: Установить MySQL

Если ещё не установлен:
- **Windows**: Скачайте [MySQL Installer](https://dev.mysql.com/downloads/installer/)
- **Linux**: `sudo apt-get install mysql-server`
- **macOS**: `brew install mysql`

### Шаг 2: Запустить MySQL

```bash
# Запустить службу MySQL (Windows)
net start MySQL80

# Linux/macOS
sudo systemctl start mysql
```

### Шаг 3: Создать базу данных

Откройте **Terminal в PyCharm** (Alt+F12) и выполните:

```bash
mysql -u root -p
```

Введите пароль MySQL, затем выполните SQL-команды:

```sql
CREATE DATABASE rukodel CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'rukodel_app'@'localhost' IDENTIFIED BY 'MyPassword123';

GRANT ALL PRIVILEGES ON rukodel.* TO 'rukodel_app'@'localhost';

FLUSH PRIVILEGES;

EXIT;
```

### Шаг 4: Настроить .env файл

1. В PyCharm откройте файл **`.env.example`**
2. Скопируйте его содержимое
3. Создайте новый файл **`.env`** (в корне проекта)
4. Вставьте содержимое и измените пароль:

```env
SECRET_KEY=django-insecure-ваш-секретный-ключ-здесь
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=rukodel
DB_USER=rukodel_app
DB_PASSWORD=MyPassword123
DB_HOST=localhost
DB_PORT=3306
```

**Как сгенерировать SECRET_KEY:**

В Terminal PyCharm выполните:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Скопируйте результат в `.env` файл.

---

## 🚀 Запуск проекта в PyCharm

### Шаг 1: Применить миграции

В **Terminal PyCharm** (Alt+F12):

```bash
python manage.py makemigrations
python manage.py migrate
```

Эта команда создаст все таблицы в базе данных MySQL.

### Шаг 2: Создать суперпользователя

```bash
python manage.py createsuperuser
```

Введите данные администратора:
- Username: `admin`
- Email: `admin@rukodel.ru`
- Password: `admin123` (или свой)

### Шаг 3: Запустить сервер

**Способ A: Через Terminal**

```bash
python manage.py runserver
```

**Способ B: Через PyCharm (удобнее)**

1. В правом верхнем углу PyCharm найдите **"Add Configuration..."**
2. Нажмите **+** → **Django Server**
3. Name: `RunServer`
4. Host: `localhost`
5. Port: `8000`
6. Нажмите **OK**
7. Нажмите зелёную кнопку **▶ Run** (Shift+F10)

### Шаг 4: Открыть сайт

В браузере откройте:
- **Админ-панель**: http://localhost:8000/admin/
- **API Products**: http://localhost:8000/api/products/
- **API Categories**: http://localhost:8000/api/categories/
- **API Masters**: http://localhost:8000/api/masters/

---

## ✅ Проверка работы

### Войдите в админ-панель

1. Откройте: http://localhost:8000/admin/
2. Войдите с данными суперпользователя
3. Вы должны увидеть разделы:
   - Пользователи
   - Мастера
   - Категории
   - Товары
   - Заказы
   - Корзина
   - Отзывы

### Создайте тестовые данные

В админ-панели:

1. **Categories** → Add → Создайте категорию:
   - Name: `Керамика`
   - Slug: `keramika`

2. **Users** → Add → Создайте пользователя-мастера:
   - Username: `master1`
   - Role: `Мастер`

3. **Masters** → Add → Создайте профиль мастера:
   - User: `master1`
   - Specialty: `Керамика`

4. **Products** → Add → Создайте товар:
   - Name: `Ваза керамическая`
   - Master: `master1`
   - Category: `Керамика`
   - Price: `2500`
   - Quantity: `5`

### Проверьте API

Откройте в браузере:
```
http://localhost:8000/api/products/
```

Вы должны увидеть JSON с созданным товаром.

---

## 🛠️ Полезные функции PyCharm

### Автодополнение Django

PyCharm автоматически распознаёт Django-проект и предоставляет:
- Автодополнение моделей
- Подсказки по Django ORM
- Подсветку шаблонов
- Навигацию по коду (Ctrl+Click)

### Django Console

**Tools → Run Django Console**

Это интерактивная консоль Python с загруженным Django:

```python
from shop.models import Product, Category

# Создать категорию
cat = Category.objects.create(name="Текстиль", slug="textil")

# Посмотреть все товары
products = Product.objects.all()
for p in products:
    print(p.name, p.price)
```

### Database Tool

1. **View → Tool Windows → Database**
2. Нажмите **+** → **Data Source** → **MySQL**
3. Введите данные подключения:
   - Host: `localhost`
   - Port: `3306`
   - Database: `rukodel`
   - User: `rukodel_app`
   - Password: `MyPassword123`
4. Нажмите **Test Connection** → **OK**

Теперь вы можете просматривать таблицы БД прямо в PyCharm!

### Запуск тестов

```bash
python manage.py test
```

---

## 🐛 Решение проблем

### Ошибка: "No module named 'shop'"

**Решение:**
- Убедитесь, что в PyCharm открыта правильная папка (корень проекта)
- Проверьте, что файл `shop/__init__.py` существует
- Перезапустите PyCharm

### Ошибка: "Access denied for user"

**Решение:**
- Проверьте данные в `.env` файле
- Убедитесь, что пользователь создан в MySQL
- Проверьте пароль

### Ошибка: "mysqlclient" не устанавливается

**Решение для Windows:**

1. Отредактируйте `requirements.txt`:
   - Замените `mysqlclient==2.2.0` на `PyMySQL==1.1.0`

2. В файле `rukodel/__init__.py` добавьте:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### Порт 8000 занят

**Решение:**

Запустите на другом порту:
```bash
python manage.py runserver 8080
```

---

## 📝 Структура проекта в PyCharm

```
rukodel-backend/
├── 📁 rukodel/               # Главный модуль проекта
│   ├── __init__.py
│   ├── settings.py          # ⚙️ Настройки
│   ├── urls.py              # 🔗 Главные URL
│   ├── wsgi.py
│   └── asgi.py
├── 📁 shop/                  # Приложение магазина
│   ├── migrations/          # 📦 Миграции БД
│   ├── __init__.py
│   ├── models.py            # 🗄️ Модели БД
│   ├── views.py             # 👁️ API Views
│   ├── serializers.py       # 📋 Сериализаторы
│   ├── admin.py             # 👤 Админ-панель
│   └── urls.py              # 🔗 URL маршруты
├── 📁 venv/                  # Виртуальное окружение
├── 📁 media/                 # Загруженные файлы
├── manage.py                # 🔧 Django утилита
├── requirements.txt         # 📦 Зависимости
├── .env                     # 🔐 Настройки (не в Git)
├── .gitignore
└── README.md
```

---

## 🎉 Готово!

Теперь вы можете:
- ✅ Редактировать код в PyCharm
- ✅ Запускать сервер одной кнопкой
- ✅ Использовать Django Console
- ✅ Просматривать БД через Database Tool
- ✅ Тестировать API

### Следующие шаги:

1. Изучите файлы `models.py`, `views.py`, `serializers.py`
2. Создайте тестовые данные через админ-панель
3. Протестируйте API через браузер или Postman
4. Подключите frontend (index.html) к API

**Нужна помощь?** Задавайте вопросы! 🚀
