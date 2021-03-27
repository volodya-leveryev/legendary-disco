from flask import redirect, render_template, request, session, url_for
from flask_admin.contrib.mongoengine import ModelView

from jimmy import models, forms


def login_required(func):
    def wrap(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrap


@login_required
def home_page():
    return render_template('home.html')


@login_required
def person_list():
    persons = models.Person.objects.order_by('last_name', 'first_name', 'second_name')
    return render_template('person_list.html', persons=persons)


@login_required
def person_edit(person_id):
    person = models.Person.objects.get_or_404(id=person_id)
    form = forms.PersonForm(obj=person)
    return render_template('person_edit.html', form=form, person=person)


@login_required
def job_assignment_list():
    job_assignments = models.JobAssignment.objects.order_by('person')
    return render_template('job_assignment_list.html', job_assignments=job_assignments)


@login_required
def student_group_list():
    student_groups = models.StudentGroup.objects.order_by('name')
    return render_template('student_group_list.html', student_groups=student_groups)


class PersonView(ModelView):
    column_list = ('fio', 'emails', 'degree', 'title')
    column_default_sort = 'last_name'
    column_labels = {
        'fio': 'ФИО',
        'emails': 'Почта',
        'degree': 'Учёная степень',
        'title': 'Учёное звание',
    }

    def is_accessible(self):
        return 'user' in session

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class TeacherView(ModelView):
    column_default_sort = 'person'
    column_labels = {
        'person': 'Преподаватель',
        'department': 'Кафедра',
        'position': 'Должность',
        'semester': 'Семестр',
        'wage_rate': 'Ставка',
    }

    def is_accessible(self):
        return 'user' in session

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class StudentGroupView(ModelView):
    column_default_sort = 'name'
    column_labels = {
        'name': 'Название',
    }

    def is_accessible(self):
        return 'user' in session

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))
