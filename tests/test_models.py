""" Тестирование моделей """
from datetime import datetime

import pytest

from jimmy.models import Course, Person, StudentGroup


@pytest.fixture
def degree1():
    """ Создание в тестовой базе ученой степени """
    degree = Person.Degree()
    degree.date = datetime(2010, 1, 1)
    degree.degree = 'к.ф.-м.н.'
    return degree


@pytest.fixture
def degree2():
    """ Создание в тестовой базе ученой степени """
    degree = Person.Degree()
    degree.date = datetime(2020, 1, 1)
    degree.degree = 'д.ф.-м.н.'
    return degree


@pytest.fixture
def title1():
    """ Создание в тестовой базе ученого звания """
    title = Person.Title()
    title.date = datetime(2010, 1, 1)
    title.title = 'доц.'
    return title


@pytest.fixture
def title2():
    """ Создание в тестовой базе ученого звания """
    title = Person.Title()
    title.date = datetime(2020, 1, 1)
    title.title = 'проф.'
    return title


@pytest.fixture
def job1():
    """ Создание в тестовой базе должности сотрудника """
    job = Person.Job()
    job.is_active = False
    job.date = datetime(2010, 1, 1)
    job.position = 'асс.'
    job.department = 'МТС'
    job.wage_rate = 0.5
    return job


@pytest.fixture
def job2():
    """ Создание в тестовой базе должности сотрудника """
    job = Person.Job()
    job.is_active = False
    job.date = datetime(2020, 1, 1)
    job.position = 'ст.пр.'
    job.department = 'ИТ'
    job.wage_rate = 1.0
    return job


@pytest.fixture
def student_group():
    """ Создание в тестовой базе учебного плана """
    group = StudentGroup()
    group.name = 'Б-ИВТ-19-1'
    group.year = 2019
    #group.program = education_program
    return group


def test_person(degree1, degree2, job1, job2, title1, title2):
    """ Проверка модельного класса для людей """
    # Строковое представление
    person = Person()
    person.last_name = 'Иванов'
    person.first_name = 'Иван'
    person.second_name = 'Иванович'
    assert person.fio == 'Иванов И.И.'
    assert str(person) == 'Иванов И.И.'

    # История присуждения ученых степеней
    person.degree_history = [degree1, degree2]
    assert person.degree == 'д.ф.-м.н.'
    person.degree_history = [degree2, degree1]
    assert person.degree == 'д.ф.-м.н.'

    # История присвоения ученых званий
    person.title_history = [title1, title2]
    assert person.title == 'проф.'
    person.title_history = [title2, title1]
    assert person.title == 'проф.'

    # История должностей сотрудника
    person.job_history = [job1, job2]
    assert person.job == ''

    # История должностей сотрудника
    job1.is_active = True
    person.job_history = [job1, job2]
    assert person.job == '0.5 асс. каф. МТС'

    # История должностей сотрудника
    job2.is_active = True
    person.job_history = [job1, job2]
    assert person.job == '1.0 ст.пр. каф. ИТ, 0.5 асс. каф. МТС'

    # История должностей сотрудника
    job1.is_active = False
    person.job_history = [job1, job2]
    assert person.job == '1.0 ст.пр. каф. ИТ'


def test_student_group(student_group):
    assert str(student_group) == 'Б-ИВТ-19-1'

    sub_groups1 = StudentGroup.Subgroups()
    sub_groups1.date = datetime(2010, 1, 1)
    sub_groups1.count = 2

    sub_groups2 = StudentGroup.Subgroups()
    sub_groups2.date = datetime(2020, 1, 1)
    sub_groups2.count = 1

    student_group.subgroups_history = [sub_groups1, sub_groups2]
    assert student_group.subgroups(4040) == 1
    student_group.subgroups_history = [sub_groups2, sub_groups1]
    assert student_group.subgroups(4020) == 2

    students1 = StudentGroup.Students()
    students1.date = datetime(2010, 1, 1)
    students1.count = 20

    students2 = StudentGroup.Students()
    students2.date = datetime(2020, 1, 1)
    students2.count = 10

    student_group.students_history = [students1, students2]
    assert student_group.students == 10
    student_group.students_history = [students2, students1]
    assert student_group.students == 10

    assert student_group.get_education_year(4040) == 1
    assert student_group.get_education_year(4041) == 2


def test_course(student_group):
    course = Course()
    course.student_group = student_group
    course.semester_abs = 4039
    course.code = 'Б1.О.01'
    course.name = 'Философия'
    assert str(course) == 'Б-ИВТ-19-1, 1: Философия'
