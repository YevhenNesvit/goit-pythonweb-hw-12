from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Вказуємо шлях до папки з шаблонами
template_path = Path("app/templates")

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
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
    await fm.send_message(message, template_name="verification.html")
