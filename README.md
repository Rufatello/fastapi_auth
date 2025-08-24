# 🚀 FastAPI Auth Service

Простой и эффективный сервис аутентификации на FastAPI с JWT токенами и PostgreSQL.

## 🛠 Технологии

- **Python 3.12** - основной язык программирования
- **FastAPI** - современный фреймворк для API
- **PostgreSQL** - реляционная база данных
- **SQLAlchemy** - ORM для работы с БД
- **Alembic** - система миграций базы данных
- **JWT** - JSON Web Tokens для аутентификации
- **Docker** - контейнеризация базы данных


## 📦 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone 
cd fastapi_auth

### 2. Настройка окружения

Создайте файл .env в корневой директории:
# Database
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=auth_db
POSTGRES_HOST=localhost
POSTGRES_PORT=6432

# JWT
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Password Hashing
HASHING_SCHEME=bcrypt

### 3. Установка зависимостей

python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

pip install -r requirements.txt

### 4. Запуск базы данных

🐳 Docker
База данных запускается в Docker контейнере:
# Запуск
docker-compose up -d

# Остановка
docker-compose down

### 5. Применение миграций

🔧 Миграции базы данных
alembic upgrade head

### 6. Запуск приложения

uvicorn main:app --reload

📚 Документация API
После запуска приложения доступна автоматическая документация:

Swagger UI: http://localhost:8000/docs
