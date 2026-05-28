#!/usr/bin/env python3
"""
Автоматический установщик проекта Django "РукоДел"
Запустите этот скрипт, чтобы создать всю структуру проекта
"""

import os
import sys

# Структура проекта с содержимым файлов
PROJECT_STRUCTURE = {
    'requirements.txt': '''Django==4.2.8
djangorestframework==3.14.0
django-cors-headers==4.3.1
PyMySQL==1.1.0
python-dotenv==1.0.0
Pillow==10.1.0
''',

    '.env.example': '''# Настройки Django
SECRET_KEY=django-insecure-change-this-in-production-12345
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Настройки базы данных MySQL
DB_NAME=rukodel
DB_USER=rukodel_app
DB_PASSWORD=YourStrongPasswordHere
DB_HOST=localhost
DB_PORT=3306
''',

    '.gitignore': '''# Python
*.py[cod]
__pycache__/
*.so
*.egg
*.egg-info/
dist/
build/
venv/
env/

# Django
*.log
db.sqlite3
media/
staticfiles/

# Environment
.env

# IDE
.idea/
.vscode/
*.swp
*.swo
*~
''',

    'manage.py': '''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rukodel.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
''',

    'rukodel/__init__.py': '''# Rukodel project
import pymysql
pymysql.install_as_MySQLdb()
''',

    'rukodel/settings.py': '''"""
Django settings for rukodel project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-this-in-production-12345')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    
    # Local apps
    'shop.apps.ShopConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rukodel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rukodel.wsgi.application'

# Database (MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'rukodel'),
        'USER': os.getenv('DB_USER', 'rukodel_app'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
]

CORS_ALLOW_CREDENTIALS = True

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# Custom user model
AUTH_USER_MODEL = 'shop.User'
''',

    'rukodel/urls.py': '''"""
Главный URL конфигурация проекта rukodel
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('shop.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

# Добавление медиа-файлов в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Настройка админ-панели
admin.site.site_header = "РукоДел - Панель администратора"
admin.site.site_title = "РукоДел Admin"
admin.site.index_title = "Управление магазином"
''',

    'rukodel/wsgi.py': '''"""
WSGI config for rukodel project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rukodel.settings')

application = get_wsgi_application()
''',

    'rukodel/asgi.py': '''"""
ASGI config for rukodel project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rukodel.settings')

application = get_asgi_application()
''',

    'shop/__init__.py': '''# Shop application
''',

    'shop/apps.py': '''from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    verbose_name = 'Магазин РукоДел'
''',

    'README.md': '''# Django Backend для «РукоДел»

## Установка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
venv\\Scripts\\activate  # Windows
source venv/bin/activate  # Linux/macOS
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте базу данных MySQL:
```sql
CREATE DATABASE rukodel CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'rukodel_app'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON rukodel.* TO 'rukodel_app'@'localhost';
FLUSH PRIVILEGES;
```

4. Настройте .env:
```bash
cp .env.example .env
# Отредактируйте .env
```

5. Примените миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

7. Запустите сервер:
```bash
python manage.py runserver
```

Админ-панель: http://localhost:8000/admin/
API: http://localhost:8000/api/
'''
}

# Файлы моделей, views, serializers и т.д. (большие файлы)
# Эти файлы нужно будет скопировать вручную или загрузить из предпросмотра

def create_file(filepath, content):
    """Создать файл с содержимым"""
    os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"✓ Создан: {filepath}")

def main():
    """Главная функция установки"""
    print("=" * 60)
    print("Установщик проекта Django 'РукоДел'")
    print("=" * 60)
    
    # Запрос директории для создания проекта
    project_dir = input("\nВведите путь для создания проекта (по умолчанию: rukodel-backend): ").strip()
    if not project_dir:
        project_dir = 'rukodel-backend'
    
    # Создание директории проекта
    if os.path.exists(project_dir):
        response = input(f"\nДиректория {project_dir} уже существует. Продолжить? (y/n): ").strip().lower()
        if response != 'y':
            print("Установка отменена.")
            sys.exit(0)
    else:
        os.makedirs(project_dir)
        print(f"\n✓ Создана директория: {project_dir}")
    
    # Переход в директорию проекта
    os.chdir(project_dir)
    
    # Создание файлов
    print("\nСоздание файлов проекта...\n")
    for filepath, content in PROJECT_STRUCTURE.items():
        create_file(filepath, content)
    
    # Создание пустых __init__.py для миграций
    create_file('shop/migrations/__init__.py', '# Migrations')
    
    print("\n" + "=" * 60)
    print("✓ Базовая структура проекта создана!")
    print("=" * 60)
    
    print("\n⚠️  ВАЖНО: Некоторые большие файлы нужно скопировать вручную:")
    print("   - shop/models.py")
    print("   - shop/views.py")
    print("   - shop/serializers.py")
    print("   - shop/admin.py")
    print("   - shop/urls.py")
    print("   - schema.sql")
    
    print("\nЭти файлы доступны в окне предпросмотра вашего чата.")
    print("Скопируйте их содержимое в соответствующие файлы проекта.")
    
    print("\n" + "=" * 60)
    print("Следующие шаги:")
    print("=" * 60)
    print("\n1. Скопируйте недостающие файлы из предпросмотра")
    print("2. Создайте виртуальное окружение:")
    print("   python -m venv venv")
    print("   venv\\Scripts\\activate  (Windows)")
    print("   source venv/bin/activate  (Linux/macOS)")
    print("\n3. Установите зависимости:")
    print("   pip install -r requirements.txt")
    print("\n4. Настройте базу данных MySQL и .env файл")
    print("\n5. Примените миграции:")
    print("   python manage.py makemigrations")
    print("   python manage.py migrate")
    print("\n6. Создайте суперпользователя:")
    print("   python manage.py createsuperuser")
    print("\n7. Запустите сервер:")
    print("   python manage.py runserver")
    
    print("\n" + "=" * 60)
    print(f"Проект создан в директории: {os.getcwd()}")
    print("=" * 60)

if __name__ == '__main__':
    main()
