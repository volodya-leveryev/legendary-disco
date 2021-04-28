import os

import pytest
from werkzeug.datastructures import FileStorage

from jimmy import create_app
from jimmy.models import Course, EducationProgram, Person, StudentGroup, db
from jimmy.views_auth import init_session


@pytest.fixture
def client():
    app = create_app()

    admin = Person()
    admin.last_name = 'admin'
    admin.first_name = 'admin'
    admin.emails = ['admin@localhost']
    admin.save()

    program = EducationProgram()
    program.code = '09.03.01'
    program.name = 'Информатика и вычислительная техника'
    program.short = 'Бак ИВТ'
    program.level = 'Бак'
    program.save()

    student_group = StudentGroup()
    student_group.name = 'ИВТ-19'
    student_group.year = 2019
    student_group.program = program
    student_group.save()

    with app.test_client() as test_client:
        yield test_client

    db.disconnect()


def test_index_page(client):
    response = client.get('/admin/')
    assert response.status_code == 200


def test_admin_load_plan(client):
    response = client.get('/admin/load_plan/')
    assert response.status_code == 302
    assert response.headers.get('Location').startswith('http://localhost/auth/login/')

    with client.session_transaction() as s:
        init_session(s, 'admin@localhost')

    response = client.get('/admin/load_plan/')
    assert response.status_code == 200
    assert 'Загрузка учебного плана'.encode('utf-8') in response.data

    assert len(Course.objects) == 0
    filename = '09030101_20-12ИВТ.plx'
    filepath = os.path.join(os.path.dirname(__file__), filename)
    response = client.post('/admin/load_plan/', data={
        'rup_file': FileStorage(stream=open(filepath, 'rb')),
        'student_group': str(StudentGroup.objects[0].id),
    })
    assert response.status_code == 302
    assert len(Course.objects) == 89

    response = client.post('/admin/load_plan/', data={
        'rup_file': FileStorage(stream=open(filepath, 'rb')),
        'student_group': str(StudentGroup.objects[0].id),
    })
    assert response.status_code == 302
    assert len(Course.objects) == 89


def test_admin_education_program(client):
    response = client.get('/admin/educationprogram/')
    assert response.status_code == 302
    assert response.headers.get('Location').startswith('http://localhost/auth/login/')

    with client.session_transaction() as s:
        init_session(s, 'admin@localhost')

    response = client.get('/admin/educationprogram/')
    assert response.status_code == 200
    assert 'Short'.encode('utf-8') in response.data
    assert 'Level'.encode('utf-8') in response.data


def test_admin_person(client):
    response = client.get('/admin/person/')
    assert response.status_code == 302
    assert response.headers.get('Location').startswith('http://localhost/auth/login/')

    with client.session_transaction() as s:
        init_session(s, 'admin@localhost')

    response = client.get('/admin/person/')
    assert response.status_code == 200
    assert 'Fio'.encode('utf-8') in response.data
    assert 'Emails'.encode('utf-8') in response.data
    assert 'Degree'.encode('utf-8') in response.data
    assert 'Title'.encode('utf-8') in response.data
    assert 'Job'.encode('utf-8') in response.data


def test_admin_student_group(client):
    response = client.get('/admin/studentgroup/')
    assert response.status_code == 302
    assert response.headers.get('Location').startswith('http://localhost/auth/login/')

    with client.session_transaction() as s:
        init_session(s, 'admin@localhost')

    response = client.get('/admin/studentgroup/')
    assert response.status_code == 200
    assert 'Program'.encode('utf-8') in response.data
    assert 'Year'.encode('utf-8') in response.data
    assert 'Subgroups'.encode('utf-8') in response.data
    assert 'Students'.encode('utf-8') in response.data


def test_admin_course(client):
    response = client.get('/admin/course/')
    assert response.status_code == 302
    assert response.headers.get('Location').startswith('http://localhost/auth/login/')

    with client.session_transaction() as s:
        init_session(s, 'admin@localhost')

    response = client.get('/admin/course/')
    assert response.status_code == 200
    assert 'Hour'.encode('utf-8') in response.data
    assert 'Semester'.encode('utf-8') in response.data
