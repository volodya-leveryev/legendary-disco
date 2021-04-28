import pytest
from werkzeug.exceptions import HTTPException

from jimmy import create_app
from jimmy.models import Person, db
from jimmy.views_auth import init_session


@pytest.fixture
def client():
    app = create_app()

    admin = Person()
    admin.last_name = 'admin'
    admin.first_name = 'admin'
    admin.emails = ['admin@localhost']
    admin.save()

    with app.test_client() as test_client:
        yield test_client

    db.disconnect()


def test_init_session(client):
    with client.session_transaction() as s:
        with pytest.raises(HTTPException):
            init_session(s, 'user@localhost')


def test_login(client):
    response = client.get('/auth/login/')
    assert response.status_code == 200
    assert 'Вход в систему'.encode('utf-8') in response.data


def test_azure_init(client):
    response = client.get('/auth/azure/init/')
    assert response.status_code == 302
    assert response.headers.get('Location').startswith('https://login.microsoftonline.com/')


def test_google_init(client):
    response = client.get('/auth/google/init/')
    assert response.status_code == 302
    assert response.headers.get('Location').startswith('https://accounts.google.com/o/oauth2/v2/auth')


def test_azure_done(client):
    response = client.get('/auth/azure/done/')
    assert response.status_code == 400


def test_google_done(client):
    response = client.get('/auth/google/done/')
    assert response.status_code == 400


def test_logout(client):
    with client.session_transaction() as s:
        init_session(s, 'admin@localhost')

    response = client.get('/auth/logout/')
    assert response.status_code == 302
    assert response.headers.get('Location').startswith('http://localhost/auth/login/')

    with client.session_transaction() as s:
        assert 'user' not in s
