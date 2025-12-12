import pytest
import smtplib

@pytest.fixture(scope="module", params=["smtp.gmail.com", "smtp.yandex.ru"])
def smtp_connection(request):
    smtp_connection = smtplib.SMTP(request.param, 587, timeout=5)
    yield smtp_connection
    print(f"finalizing {smtp_connection}")
    smtp_connection.close()

def test_smtp_connection(smtp_connection):
    assert smtp_connection

@pytest.mark.parametrize("conn", ["smtp.gmail.com", "smtp.yandex.ru"])
def test_smtp_connection_parametrized(conn):
    smtp_connection = None
    try:
        smtp_connection = smtplib.SMTP(conn, 587, timeout=5)
        assert smtp_connection
    finally:
        if not smtp_connection:
            return
        print(f"finalizing {smtp_connection}")
        smtp_connection.close()

