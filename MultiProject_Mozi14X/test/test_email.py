#test_email.py
import sys
import os
import pytest
from unittest.mock import patch
from email.message import EmailMessage

# Projekt gyökér hozzáadása a path-hoz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.email_utils import send_email

def test_send_email_mock():
    """Alap SMTP mock teszt"""
    with patch("backend.services.email_service.smtplib.SMTP") as mock_smtp:
        send_email("Teszt tárgy", "Teszt üzenet", ["teszt@example.com"])
        instance = mock_smtp.return_value.__enter__.return_value
        instance.send_message.assert_called_once()


def test_send_email_mock_with_content():
    """SMTP mock + tárgy és body ellenőrzés"""
    subject = "Teszt tárgy"
    body = "Ez a teszt üzenet tartalma"
    to = ["a@example.com"]

    with patch("backend.services.email_service.smtplib.SMTP") as mock_smtp:
        send_email(subject, body, to)
        instance = mock_smtp.return_value.__enter__.return_value
        instance.send_message.assert_called_once()

        # EmailMessage objektum kinyerése
        sent_msg: EmailMessage = instance.send_message.call_args[0][0]

        # Tárgy és tartalom ellenőrzése
        assert sent_msg['Subject'] == subject
        assert sent_msg.get_content().strip() == body
