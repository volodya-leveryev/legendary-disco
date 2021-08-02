import pytest

from jimmy import create_app
from jimmy.models import Person, StudentGroup, db


@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'secret',
        'MONGODB_HOST': 'mongomock://localhost',
        'MONGODB_DB': 'jimmy',
    })

    admin = Person()
    admin.last_name = 'admin'
    admin.first_name = 'admin'
    admin.emails = ['admin@localhost']
    admin.save()

    student_group = StudentGroup()
    student_group.name = 'ИВТ-19'
    student_group.year = 2019
    student_group.program_code = '09.03.01'
    student_group.program_name = 'Информатика и вычислительная техника'
    student_group.level = 'Бак'
    student_group.save()

    with app.test_client() as test_client:
        yield test_client

    db.disconnect()
