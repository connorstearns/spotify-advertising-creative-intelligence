import logging

from src.access_control import AUTHENTICATED_KEY, access_is_granted


def test_missing_password_allows_access_and_logs_warning(caplog):
    session = {}
    with caplog.at_level(logging.WARNING):
        assert access_is_granted({}, session)

    assert session[AUTHENTICATED_KEY] is True
    assert "allowing local demo access" in caplog.text


def test_incorrect_password_is_rejected():
    session = {}

    assert not access_is_granted({"app_password": "correct"}, session, "incorrect")
    assert AUTHENTICATED_KEY not in session


def test_correct_password_authenticates_session():
    session = {}

    assert access_is_granted({"app_password": "correct"}, session, "correct")
    assert session[AUTHENTICATED_KEY] is True


def test_authenticated_session_does_not_require_password_again():
    session = {AUTHENTICATED_KEY: True}

    assert access_is_granted({"app_password": "correct"}, session)
