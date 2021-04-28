import pytest

from jimmy import create_app
from jimmy.models import Person, db
from jimmy.views import semester_filter
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


def test_semester_filter():
    assert semester_filter(0) == '2021, весна'
    assert semester_filter(4000) == '2000, весна'


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers.get('Location') == 'http://localhost/auth/login/'

    with client.session_transaction() as s:
        init_session(s, 'admin@localhost')

    response = client.get('/')
    assert response.status_code == 200
    assert 'Карточка учебных поручений'.encode('utf-8') in response.data


def test_semester_view(client):
    with client.session_transaction() as s:
        init_session(s, 'admin@localhost')

    response = client.get('/semester/2000/1/')
    assert response.status_code == 302
    assert response.headers.get('Location') == 'http://localhost/'

    with client.session_transaction() as s:
        assert s['sem'] == 4000
