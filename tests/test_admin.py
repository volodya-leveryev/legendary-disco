import pytest

from jimmy import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client


def test_index_page(client):
    """ Админка: главная страница """
    response = client.get('/admin/')
    assert response.status_code == 200


def test_admin_load_plan(client):
    """ Админка: программы обучения """
    response = client.get('/admin/load_plan/')
    assert response.status_code == 302


def test_admin_education_program(client):
    """ Админка: программы обучения """
    response = client.get('/admin/educationprogram/')
    assert response.status_code == 302


def test_admin_course(client):
    """ Админка: курс обучения """
    response = client.get('/admin/course/')
    assert response.status_code == 302


def test_admin_person(client):
    """ Админка: человек """
    response = client.get('/admin/person/')
    assert response.status_code == 302


def test_admin_student_group(client):
    """ Админка: учебная группа """
    response = client.get('/admin/studentgroup/')
    assert response.status_code == 302
