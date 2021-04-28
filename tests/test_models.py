from datetime import datetime

import pytest

from jimmy.models import Course, EducationProgram, Person, StudentGroup


@pytest.fixture
def degree1():
    d1 = Person.Degree()
    d1.date = datetime(2010, 1, 1)
    d1.degree = 'к.ф.-м.н.'
    return d1


@pytest.fixture
def degree2():
    d2 = Person.Degree()
    d2.date = datetime(2020, 1, 1)
    d2.degree = 'д.ф.-м.н.'
    return d2


@pytest.fixture
def title1():
    t1 = Person.Title()
    t1.date = datetime(2010, 1, 1)
    t1.title = 'доц.'
    return t1


@pytest.fixture
def title2():
    t2 = Person.Title()
    t2.date = datetime(2020, 1, 1)
    t2.title = 'проф.'
    return t2


@pytest.fixture
def job1():
    j = Person.Job()
    j.is_active = False
    j.date = datetime(2010, 1, 1)
    j.position = 'асс.'
    j.department = 'МТС'
    j.wage_rate = 0.5
    return j


@pytest.fixture
def job2():
    j = Person.Job()
    j.is_active = False
    j.date = datetime(2020, 1, 1)
    j.position = 'ст.пр.'
    j.department = 'ИТ'
    j.wage_rate = 1.0
    return j


@pytest.fixture
def education_program():
    ep = EducationProgram()
    ep.code = '09.03.01'
    ep.name = 'Информатика и вычислительная техника'
    ep.short = 'ИВТ'
    ep.level = 'Бак.'
    return ep


@pytest.fixture
def student_group(education_program):
    sg = StudentGroup()
    sg.name = 'Б-ИВТ-19-1'
    sg.year = 2019
    sg.program = education_program
    return sg


def test_person(degree1, degree2, job1, job2, title1, title2):
    person = Person()
    person.last_name = 'Иванов'
    person.first_name = 'Иван'
    person.second_name = 'Иванович'
    assert person.fio == 'Иванов И.И.'
    assert str(person) == 'Иванов И.И.'

    person.degree_history = [degree1, degree2]
    assert person.degree == 'д.ф.-м.н.'
    person.degree_history = [degree2, degree1]
    assert person.degree == 'д.ф.-м.н.'

    person.title_history = [title1, title2]
    assert person.title == 'проф.'
    person.title_history = [title2, title1]
    assert person.title == 'проф.'

    person.job_history = [job1, job2]
    assert person.job == ''

    job1.is_active = True
    person.job_history = [job1, job2]
    assert person.job == '0.5 асс. каф. МТС'

    job2.is_active = True
    person.job_history = [job1, job2]
    assert person.job == '1.0 ст.пр. каф. ИТ, 0.5 асс. каф. МТС'

    job1.is_active = False
    person.job_history = [job1, job2]
    assert person.job == '1.0 ст.пр. каф. ИТ'


def test_education_program(education_program):
    assert str(education_program) == 'Бак. ИВТ'


def test_student_group(student_group):
    assert str(student_group) == 'Б-ИВТ-19-1'

    sub_groups1 = StudentGroup.Subgroups()
    sub_groups1.date = datetime(2010, 1, 1)
    sub_groups1.count = 2

    sub_groups2 = StudentGroup.Subgroups()
    sub_groups2.date = datetime(2020, 1, 1)
    sub_groups2.count = 1

    student_group.subgroups_history = [sub_groups1, sub_groups2]
    assert student_group.subgroups == 1
    student_group.subgroups_history = [sub_groups2, sub_groups1]
    assert student_group.subgroups == 1

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
    course.semester = 4039
    course.code = 'Б1.О.01'
    course.name = 'Философия'
    assert str(course) == 'Б-ИВТ-19-1, 1: Философия'
