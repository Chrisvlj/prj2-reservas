import os
import smtplib
from email.message import EmailMessage


def despachar(destinatario: str, asunto: str, cuerpo: str, transporte=None) -> str:
    """Devuelve pendiente, enviada o error. No lanza si el envío falla."""
    if transporte is not None:
        try:
            transporte(destinatario, asunto, cuerpo)
        except Exception:
            return "error"
        return "enviada"
    url = os.environ.get("SMTP_URL", "").strip()
    if not url:
        return "pendiente"
    try:
        _enviar_smtp(url, destinatario, asunto, cuerpo)
    except Exception:
        return "error"
    return "enviada"


def _enviar_smtp(url: str, destinatario: str, asunto: str, cuerpo: str) -> None:
    from urllib.parse import urlparse

    parsed = urlparse(url)
    host = parsed.hostname or "localhost"
    port = parsed.port or 25
    mensaje = EmailMessage()
    mensaje["From"] = parsed.username or "reservas@localhost"
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.set_content(cuerpo)
    with smtplib.SMTP(host, port, timeout=5) as smtp:
        if parsed.username and parsed.password:
            smtp.starttls()
            smtp.login(parsed.username, parsed.password)
        smtp.send_message(mensaje)
