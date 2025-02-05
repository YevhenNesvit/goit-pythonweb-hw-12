from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pathlib import Path
from ..config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM
import os

# Вказуємо шлях до папки з шаблонами
template_path = Path("app/templates")

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=465,
    MAIL_SERVER="smtp.meta.ua",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=template_path,  # Додаємо шлях до шаблонів
)


async def send_verification_email(email: str, token: str):
    verification_url = f"http://localhost:8000/auth/verify/{token}"

    message = MessageSchema(
        subject="Verify your email",
        recipients=[email],
        template_body={"verification_url": verification_url},
        subtype="html",
    )

    fm = FastMail(conf)
    fm.send_message(message, template_name="verification.html")


async def send_password_reset_email(email: str, token: str):
    reset_url = f"http://localhost:8000/auth/reset-password?token={token}"

    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email],
        template_body={"reset_url": reset_url},
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="password_reset.html")
