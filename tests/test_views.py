""" Тестирование страниц """

from jimmy.views import semester_filter
from jimmy.views_auth import init_session


def test_semester_filter():
    """ Фильтр для представления семестра в шаблонах Jinja2 """
    assert semester_filter(0) == '0, весна'
    assert semester_filter(4000) == '2000, весна'


def test_home_page(client):
    """ Карточка учебных поручений """
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers.get('Location') == 'http://localhost/auth/login/'

    with client.session_transaction() as s:
        init_session('admin@localhost', s)

    response = client.get('/')
    assert response.status_code == 200
    assert 'Карточка учебных поручений'.encode('utf-8') in response.data


def test_semester_view(client):
    """ Переход к другому семестру """
    with client.session_transaction() as s:
        init_session('admin@localhost', s)

    response = client.get('/semester/2000/1/')
    assert response.status_code == 302
    assert response.headers.get('Location') == 'http://localhost/'

    with client.session_transaction() as s:
        assert s['sem'] == 4000
