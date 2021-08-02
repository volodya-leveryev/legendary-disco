import pytest
from werkzeug.exceptions import HTTPException

from jimmy.views_auth import init_session


def test_init_session(client):
    with client.session_transaction() as s:
        with pytest.raises(HTTPException):
            init_session('user@localhost', s)


def test_login(client):
    response = client.get('/auth/login/')
    assert response.status_code == 200
    assert 'Вход в систему'.encode('utf-8') in response.data


def test_azure_done(client):
    response = client.get('/auth/azure/done/')
    assert response.status_code == 400


def test_google_done(client):
    response = client.get('/auth/google/done/')
    assert response.status_code == 400


def test_logout(client):
    with client.session_transaction() as s:
        init_session('admin@localhost', s)

    response = client.get('/auth/logout/')
    assert response.status_code == 302
    assert response.headers.get('Location').startswith('http://localhost/auth/login/')

    with client.session_transaction() as s:
        assert 'user' not in s
