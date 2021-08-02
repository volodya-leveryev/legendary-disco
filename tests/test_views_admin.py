""" Тестирование HTML-страниц для админки """
import os

import pytest
from werkzeug.datastructures import FileStorage

from jimmy import create_app
from jimmy.models import Course, Person, StudentGroup, db
from jimmy.views_auth import init_session


def test_index_page(client):
    """ Главная страница админки """
    response = client.get('/admin/')
    assert response.status_code == 200


def test_admin_load_plan(client):
    """ Страница загрузки РУП """
    response = client.get('/admin/load_plan/')
    assert response.status_code == 302
    assert response.headers.get('Location').startswith('http://localhost/auth/login/')

    with client.session_transaction() as s:
        init_session('admin@localhost', s)

    response = client.get('/admin/load_plan/')
    assert response.status_code == 200
    assert 'Загрузка учебного плана'.encode('utf-8') in response.data

    assert len(Course.objects) == 0
    filename = '09030101_20-12ИВТ.plx'
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'rb') as stream:
        response = client.post('/admin/load_plan/', data={
            'rup_file': FileStorage(stream=stream),
            'student_group': str(StudentGroup.objects[0].id),
        })
    assert response.status_code == 302
    assert len(Course.objects) == 89

    with open(filepath, 'rb') as stream:
        response = client.post('/admin/load_plan/', data={
            'rup_file': FileStorage(stream=stream),
            'student_group': str(StudentGroup.objects[0].id),
        })
    assert response.status_code == 302
    assert len(Course.objects) == 89


def test_admin_person(client):
    """ Страница администрирования людей """
    response = client.get('/admin/person/')
    assert response.status_code == 302
    assert response.headers.get('Location').startswith('http://localhost/auth/login/')

    with client.session_transaction() as s:
        init_session('admin@localhost', s)

    response = client.get('/admin/person/')
    assert response.status_code == 200
    assert 'Fio'.encode('utf-8') in response.data
    assert 'Emails'.encode('utf-8') in response.data
    # assert 'Degree'.encode('utf-8') in response.data
    # assert 'Title'.encode('utf-8') in response.data
    assert 'Job'.encode('utf-8') in response.data


def test_admin_student_group(client):
    """ Страница администрирования студенческих групп """
    response = client.get('/admin/studentgroup/')
    assert response.status_code == 302
    assert response.headers.get('Location').startswith('http://localhost/auth/login/')

    with client.session_transaction() as s:
        init_session('admin@localhost', s)

    response = client.get('/admin/studentgroup/')
    assert response.status_code == 200
    assert 'Program'.encode('utf-8') in response.data
    assert 'Year'.encode('utf-8') in response.data


def test_admin_course(client):
    """ Страница администрирования курсов обучения """
    response = client.get('/admin/course/')
    assert response.status_code == 302
    assert response.headers.get('Location').startswith('http://localhost/auth/login/')

    with client.session_transaction() as s:
        init_session('admin@localhost', s)

    response = client.get('/admin/course/')
    assert response.status_code == 200
    assert 'Hour'.encode('utf-8') in response.data
    assert 'Semester'.encode('utf-8') in response.data
