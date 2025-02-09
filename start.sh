#!/bin/sh
alembic revision --autogenerate -m \"Initial migration\"
alembic upgrade head  # Виконує всі міграції
uvicorn app.main:app --host 0.0.0.0 --port 8000  # Запускає сервер