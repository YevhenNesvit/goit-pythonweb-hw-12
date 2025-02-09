# Contacts management API

## Опис
Цей проєкт використовує FastAPI, PostgreSQL та Redis. Він включає систему міграцій бази даних з Alembic та контейнеризацію через Docker.

## Структура проєкту
- **FastAPI** – бекенд API
- **PostgreSQL** – база даних
- **Redis** – кешування та черги повідомлень
- **Alembic** – управління міграціями бази даних
- **Docker** – контейнеризація та розгортання

## Локальний запуск
1. **Клонуйте репозиторій**
   ```sh
   git clone https://github.com/YevhenNesvit/goit-pythonweb-hw-12
   cd your-repo
   ```
2. **Створіть `.env` файл та додайте змінні оточення**
   ```ini
    DATABASE_URL
    SECRET_KEY
    ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES

    MAIL_USERNAME
    MAIL_PASSWORD
    MAIL_FROM

    CLOUDINARY_CLOUD_NAME
    CLOUDINARY_API_KEY
    CLOUDINARY_API_SECRET

    REDIS_HOST
    REDIS_PORT
   ```
3. **Запустіть Docker-контейнери**
   ```sh
   docker-compose up --build
   ```
4. **API буде доступне за адресою:** `https://contacts-n7n0.onrender.com/docs`

5. **Адмін юзер для тестування**
    ```sh
    login - admin@example.com
    password - admin
    ```
## Автор
- [Євген Несвіт](https://github.com/YevhenNesvit/goit-pythonweb-hw-12)
